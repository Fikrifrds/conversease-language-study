"use client";

import { useEffect, useMemo, useState } from "react";
import {
  ChevronDown,
  ChevronUp,
  MailCheck,
  MailX,
  RefreshCcw,
  Search,
  ShieldAlert,
  ShieldMinus,
  ShieldPlus,
  Trash2,
  UsersRound
} from "lucide-react";
import type { AuthUser } from "@/lib/auth-api";
import {
  bulkDeleteAdminUsers,
  deleteAdminUser,
  listAdminUsers,
  updateAdminUserRole,
  type AdminUser
} from "@/lib/admin-users-api";

function formatDate(value: string | null) {
  if (!value) {
    return "-";
  }

  return new Intl.DateTimeFormat("id-ID", {
    day: "numeric",
    month: "short",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit"
  }).format(new Date(value));
}

function roleTone(role: AdminUser["role"]) {
  return role === "admin" ? "bg-mint text-leaf" : "bg-paper text-ink/65";
}

function isUserDeletable(user: AdminUser, currentAdminId: string) {
  return user.role !== "admin" && user.id !== currentAdminId;
}

function dateValue(value: string) {
  return new Date(value).getTime();
}

export function AdminUsersManager({ adminUser }: { adminUser: AuthUser }) {
  const [users, setUsers] = useState<AdminUser[]>([]);
  const [search, setSearch] = useState("");
  const [roleFilter, setRoleFilter] = useState<"all" | "admin" | "student">("all");
  const [verificationFilter, setVerificationFilter] = useState<"all" | "verified" | "unverified">("all");
  const [sortBy, setSortBy] = useState<"updated_desc" | "updated_asc" | "name_asc" | "name_desc">("updated_desc");
  const [selectedUserIds, setSelectedUserIds] = useState<string[]>([]);
  const [selectedUserId, setSelectedUserId] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [actionUserId, setActionUserId] = useState<string | null>(null);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    void loadUsers();
    // Load once when this admin screen opens.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const filteredUsers = useMemo(() => {
    const nextUsers = users.filter((user) => {
      if (roleFilter !== "all" && user.role !== roleFilter) {
        return false;
      }
      if (verificationFilter === "verified" && !user.emailVerifiedAt) {
        return false;
      }
      if (verificationFilter === "unverified" && user.emailVerifiedAt) {
        return false;
      }
      return true;
    });

    nextUsers.sort((left, right) => {
      if (sortBy === "updated_asc") {
        return dateValue(left.updatedAt) - dateValue(right.updatedAt);
      }
      if (sortBy === "name_asc") {
        return (left.name || left.email).localeCompare(right.name || right.email, "id");
      }
      if (sortBy === "name_desc") {
        return (right.name || right.email).localeCompare(left.name || left.email, "id");
      }
      return dateValue(right.updatedAt) - dateValue(left.updatedAt);
    });

    return nextUsers;
  }, [roleFilter, sortBy, users, verificationFilter]);

  const totals = useMemo(() => {
    return filteredUsers.reduce(
      (acc, user) => {
        acc.count += 1;
        if (user.role === "admin") {
          acc.admin += 1;
        }
        if (user.emailVerifiedAt) {
          acc.verified += 1;
        } else {
          acc.unverified += 1;
        }
        return acc;
      },
      { admin: 0, count: 0, unverified: 0, verified: 0 }
    );
  }, [filteredUsers]);

  const deletableUsers = useMemo(
    () => filteredUsers.filter((user) => isUserDeletable(user, adminUser.id)),
    [adminUser.id, filteredUsers]
  );

  async function loadUsers(nextSearch = search) {
    setIsLoading(true);
    setMessage("");
    setError("");

    try {
      const nextUsers = await listAdminUsers({
        search: nextSearch.trim(),
        limit: 200
      });
      setUsers(nextUsers);
      setSelectedUserIds((current) => current.filter((userId) => nextUsers.some((user) => user.id === userId)));
      setSelectedUserId((current) => (current && nextUsers.some((user) => user.id === current) ? current : null));
      setMessage(nextUsers.length ? `${nextUsers.length} user dimuat.` : "Tidak ada user pada pencarian ini.");
    } catch {
      setError("User belum bisa dimuat. Pastikan akunmu punya role admin atau cek koneksi API.");
    } finally {
      setIsLoading(false);
    }
  }

  async function updateRole(user: AdminUser, role: AdminUser["role"]) {
    setActionUserId(user.id);
    setMessage("");
    setError("");

    try {
      const updated = await updateAdminUserRole({ userId: user.id, role });
      setUsers((current) => current.map((item) => (item.id === updated.id ? updated : item)));
      setSelectedUserId(updated.id);
      setMessage(role === "admin" ? `${updated.email} sekarang admin.` : `${updated.email} kembali menjadi student.`);
    } catch {
      setError("Role belum bisa diubah. Admin tidak bisa mencabut role admin dirinya sendiri.");
    } finally {
      setActionUserId(null);
    }
  }

  async function removeUser(user: AdminUser) {
    if (!isUserDeletable(user, adminUser.id)) {
      setError("Akun admin tidak bisa dihapus dari halaman ini.");
      return;
    }

    const confirmed = window.confirm(
      `Hapus user ${user.email}? Semua data terkait user ini juga ikut terhapus.`
    );
    if (!confirmed) {
      return;
    }

    setActionUserId(user.id);
    setMessage("");
    setError("");

    try {
      await deleteAdminUser({ userId: user.id });
      setUsers((current) => current.filter((item) => item.id !== user.id));
      setSelectedUserIds((current) => current.filter((item) => item !== user.id));
      setSelectedUserId((current) => (current === user.id ? null : current));
      setMessage(`${user.email} berhasil dihapus.`);
    } catch {
      setError("User belum bisa dihapus. Pastikan user tersebut bukan admin.");
    } finally {
      setActionUserId(null);
    }
  }

  async function removeSelectedUsers() {
    if (!selectedUserIds.length) {
      return;
    }

    const confirmed = window.confirm(
      `Hapus ${selectedUserIds.length} user terpilih? Semua data terkait user ini juga ikut terhapus.`
    );
    if (!confirmed) {
      return;
    }

    setActionUserId("bulk-delete");
    setMessage("");
    setError("");

    try {
      const result = await bulkDeleteAdminUsers({ userIds: selectedUserIds });
      setUsers((current) => current.filter((item) => !result.userIds.includes(item.id)));
      setSelectedUserIds([]);
      setSelectedUserId((current) => (current && result.userIds.includes(current) ? null : current));
      setMessage(`${result.deleted} user berhasil dihapus.`);
    } catch {
      setError("Bulk delete gagal. Pastikan daftar yang dipilih tidak berisi admin.");
    } finally {
      setActionUserId(null);
    }
  }

  return (
    <section className="space-y-5">
      <div className="rounded-lg border border-ink/10 bg-white p-5 shadow-sm">
        <div className="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
          <div className="flex items-start gap-3">
            <div className="grid h-10 w-10 place-items-center rounded-lg bg-mint">
              <UsersRound className="h-5 w-5 text-leaf" aria-hidden="true" />
            </div>
            <div>
              <p className="text-sm font-semibold uppercase text-leaf">Admin Users</p>
              <h1 className="mt-1 text-2xl font-semibold">User Access</h1>
              <p className="mt-2 text-sm leading-6 text-ink/60">
                Kelola role admin dan hapus user tanpa membuka database.
              </p>
            </div>
          </div>

          <div className="rounded-lg bg-mint px-4 py-3 text-sm text-ink/70">
            Login sebagai <span className="font-semibold text-ink">{adminUser.email}</span>
          </div>
        </div>

        <div className="mt-5 flex flex-col gap-3 lg:flex-row">
          <div className="flex flex-1 gap-2">
            <input
              type="search"
              value={search}
              onChange={(event) => setSearch(event.target.value)}
              onKeyDown={(event) => {
                if (event.key === "Enter") {
                  void loadUsers();
                }
              }}
              className="focus-ring min-w-0 flex-1 rounded-lg border border-ink/15 bg-white px-3 py-2 text-sm text-ink"
              placeholder="Cari nama atau email"
            />
            <button
              type="button"
              onClick={() => loadUsers()}
              disabled={isLoading}
              className="focus-ring inline-flex h-10 items-center justify-center gap-2 rounded-lg bg-ink px-4 text-sm font-semibold text-white disabled:cursor-not-allowed disabled:opacity-60"
            >
              <Search className="h-4 w-4" aria-hidden="true" />
              Cari
            </button>
          </div>

          <button
            type="button"
            onClick={() => loadUsers()}
            disabled={isLoading}
            className="focus-ring inline-flex h-10 items-center justify-center gap-2 rounded-lg border border-ink/10 bg-white px-4 text-sm font-semibold text-ink disabled:cursor-not-allowed disabled:opacity-60"
          >
            <RefreshCcw className="h-4 w-4" aria-hidden="true" />
            Refresh
          </button>
        </div>

        <div className="mt-4 grid gap-2 sm:grid-cols-2 xl:grid-cols-4">
          <Metric label="Users" value={totals.count} />
          <Metric label="Admins" value={totals.admin} />
          <Metric label="Verified" value={totals.verified} />
          <Metric label="Unverified" value={totals.unverified} />
        </div>

        <div className="mt-4 grid gap-2 lg:grid-cols-3">
          <select
            value={roleFilter}
            onChange={(event) => setRoleFilter(event.target.value as "all" | "admin" | "student")}
            className="focus-ring rounded-lg border border-ink/15 bg-white px-3 py-2 text-sm text-ink"
          >
            <option value="all">Semua role</option>
            <option value="admin">Admin</option>
            <option value="student">Student</option>
          </select>

          <select
            value={verificationFilter}
            onChange={(event) =>
              setVerificationFilter(event.target.value as "all" | "verified" | "unverified")
            }
            className="focus-ring rounded-lg border border-ink/15 bg-white px-3 py-2 text-sm text-ink"
          >
            <option value="all">Semua email</option>
            <option value="verified">Email verified</option>
            <option value="unverified">Belum verified</option>
          </select>

          <select
            value={sortBy}
            onChange={(event) =>
              setSortBy(event.target.value as "updated_desc" | "updated_asc" | "name_asc" | "name_desc")
            }
            className="focus-ring rounded-lg border border-ink/15 bg-white px-3 py-2 text-sm text-ink"
          >
            <option value="updated_desc">Terbaru diupdate</option>
            <option value="updated_asc">Terlama diupdate</option>
            <option value="name_asc">Nama A-Z</option>
            <option value="name_desc">Nama Z-A</option>
          </select>
        </div>

        {message ? <p className="mt-4 rounded-lg bg-mint px-4 py-3 text-sm text-ink/70">{message}</p> : null}
        {error ? <p className="mt-4 rounded-lg bg-[#fde7df] px-4 py-3 text-sm text-ink/70">{error}</p> : null}
      </div>

      <div className="rounded-lg border border-ink/10 bg-white p-5 shadow-sm">
        <div className="flex flex-col gap-3 lg:flex-row lg:items-center lg:justify-between">
          <div>
            <h2 className="font-semibold">Users</h2>
            <p className="mt-1 text-sm text-ink/55">{filteredUsers.length} user ditampilkan.</p>
          </div>

          <div className="flex flex-wrap gap-2">
            <button
              type="button"
              onClick={() => setSelectedUserIds(deletableUsers.map((user) => user.id))}
              disabled={!deletableUsers.length}
              className="focus-ring rounded-lg border border-ink/10 px-3 py-2 text-sm font-semibold text-ink disabled:cursor-not-allowed disabled:opacity-60"
            >
              Pilih semua
            </button>
            <button
              type="button"
              onClick={() => setSelectedUserIds([])}
              disabled={!selectedUserIds.length}
              className="focus-ring rounded-lg border border-ink/10 px-3 py-2 text-sm font-semibold text-ink disabled:cursor-not-allowed disabled:opacity-60"
            >
              Reset pilih
            </button>
            <button
              type="button"
              onClick={removeSelectedUsers}
              disabled={!selectedUserIds.length || actionUserId === "bulk-delete"}
              className="focus-ring inline-flex items-center gap-2 rounded-lg border border-coral px-3 py-2 text-sm font-semibold text-coral disabled:cursor-not-allowed disabled:opacity-60"
            >
              <Trash2 className="h-4 w-4" aria-hidden="true" />
              {actionUserId === "bulk-delete" ? "Menghapus..." : `Hapus ${selectedUserIds.length}`}
            </button>
          </div>
        </div>

        <div className="mt-4 space-y-3">
          {filteredUsers.map((user) => {
            const canDelete = isUserDeletable(user, adminUser.id);
            const isChecked = selectedUserIds.includes(user.id);
            const isOpen = selectedUserId === user.id;

            return (
              <article
                key={user.id}
                className={`rounded-lg border transition ${
                  isOpen ? "border-leaf bg-mint" : "border-ink/10 bg-paper"
                }`}
              >
                <div className="flex flex-col gap-4 p-4 lg:flex-row lg:items-start">
                  <div className="flex items-start gap-3 lg:flex-1">
                    <input
                      type="checkbox"
                      checked={isChecked}
                      disabled={!canDelete}
                      onChange={(event) => {
                        if (event.target.checked) {
                          setSelectedUserIds((current) => (current.includes(user.id) ? current : [...current, user.id]));
                          return;
                        }
                        setSelectedUserIds((current) => current.filter((item) => item !== user.id));
                      }}
                      className="mt-1"
                    />

                    <div className="min-w-0 flex-1">
                      <div className="flex flex-col gap-3 md:flex-row md:items-start md:justify-between">
                        <div className="min-w-0">
                          <p className="truncate font-semibold">{user.name || user.email}</p>
                          <p className="mt-1 truncate text-sm text-ink/60">{user.email}</p>
                        </div>
                        <span className={`w-fit rounded-md px-2 py-1 text-xs font-semibold ${roleTone(user.role)}`}>
                          {user.role}
                        </span>
                      </div>

                      <div className="mt-3 flex flex-wrap gap-2">
                        <StatusBadge
                          icon={user.emailVerifiedAt ? MailCheck : MailX}
                          label={user.emailVerifiedAt ? "verified" : "unverified"}
                          tone={user.emailVerifiedAt ? "bg-mint text-leaf" : "bg-[#fde7df] text-coral"}
                        />
                        {user.looksSuspicious ? (
                          <StatusBadge
                            icon={ShieldAlert}
                            label="suspicious"
                            tone="bg-[#fde7df] text-coral"
                          />
                        ) : null}
                      </div>

                      <p className="mt-3 text-xs text-ink/50">Updated {formatDate(user.updatedAt)}</p>
                    </div>
                  </div>

                  <button
                    type="button"
                    onClick={() => setSelectedUserId((current) => (current === user.id ? null : user.id))}
                    className="focus-ring inline-flex items-center justify-center gap-2 rounded-lg border border-ink/10 bg-white px-3 py-2 text-sm font-semibold text-ink"
                  >
                    {isOpen ? <ChevronUp className="h-4 w-4" aria-hidden="true" /> : <ChevronDown className="h-4 w-4" aria-hidden="true" />}
                    {isOpen ? "Tutup detail" : "Lihat detail"}
                  </button>
                </div>

                {isOpen ? (
                  <div className="border-t border-ink/10 px-4 py-4">
                    <UserDetail
                      user={user}
                      currentAdminId={adminUser.id}
                      isActing={actionUserId === user.id}
                      canDelete={canDelete}
                      onPromote={() => updateRole(user, "admin")}
                      onDemote={() => updateRole(user, "student")}
                      onDelete={() => removeUser(user)}
                    />
                  </div>
                ) : null}
              </article>
            );
          })}

          {!filteredUsers.length ? (
            <div className="rounded-lg bg-paper p-5 text-sm leading-6 text-ink/60">
              Tidak ada user yang cocok dengan pencarian atau filter ini.
            </div>
          ) : null}
        </div>
      </div>
    </section>
  );
}

function UserDetail({
  user,
  currentAdminId,
  isActing,
  canDelete,
  onPromote,
  onDemote,
  onDelete
}: {
  user: AdminUser;
  currentAdminId: string;
  isActing: boolean;
  canDelete: boolean;
  onPromote: () => void;
  onDemote: () => void;
  onDelete: () => void;
}) {
  const isCurrentAdmin = user.id === currentAdminId;

  return (
    <div>
      <div className="flex flex-col gap-3 md:flex-row md:items-start md:justify-between">
        <div className="min-w-0">
          <p className="text-sm font-semibold uppercase text-leaf">User Detail</p>
          <h2 className="mt-2 break-words text-2xl font-semibold">{user.name || user.email}</h2>
          <p className="mt-1 break-words text-sm text-ink/55">{user.email}</p>
        </div>
        <span className={`rounded-md px-3 py-2 text-sm font-semibold ${roleTone(user.role)}`}>
          {user.role}
        </span>
      </div>

      <dl className="mt-5 grid gap-3 md:grid-cols-2 xl:grid-cols-4">
        <DetailItem label="User ID" value={user.id} />
        <DetailItem label="Email verified" value={formatDate(user.emailVerifiedAt)} />
        <DetailItem label="Created" value={formatDate(user.createdAt)} />
        <DetailItem label="Updated" value={formatDate(user.updatedAt)} />
      </dl>

      <div className="mt-5 flex flex-wrap gap-2">
        <StatusBadge
          icon={user.emailVerifiedAt ? MailCheck : MailX}
          label={user.emailVerifiedAt ? "Email verified" : "Belum verified"}
          tone={user.emailVerifiedAt ? "bg-mint text-leaf" : "bg-[#fde7df] text-coral"}
        />
        {user.looksSuspicious ? (
          <StatusBadge icon={ShieldAlert} label="Nama mencurigakan" tone="bg-[#fde7df] text-coral" />
        ) : null}
      </div>

      <div className="mt-5 grid gap-3 lg:grid-cols-3">
        <button
          type="button"
          onClick={onPromote}
          disabled={user.role === "admin" || isActing}
          className="focus-ring inline-flex min-h-12 items-center justify-center gap-2 rounded-lg bg-ink px-4 text-sm font-semibold text-white disabled:cursor-not-allowed disabled:opacity-60"
        >
          <ShieldPlus className="h-4 w-4" aria-hidden="true" />
          {isActing ? "Processing" : "Make Admin"}
        </button>
        <button
          type="button"
          onClick={onDemote}
          disabled={user.role !== "admin" || isCurrentAdmin || isActing}
          className="focus-ring inline-flex min-h-12 items-center justify-center gap-2 rounded-lg border border-coral px-4 text-sm font-semibold text-coral disabled:cursor-not-allowed disabled:opacity-60"
        >
          <ShieldMinus className="h-4 w-4" aria-hidden="true" />
          Remove Admin
        </button>
        <button
          type="button"
          onClick={onDelete}
          disabled={!canDelete || isActing}
          className="focus-ring inline-flex min-h-12 items-center justify-center gap-2 rounded-lg border border-coral px-4 text-sm font-semibold text-coral disabled:cursor-not-allowed disabled:opacity-60"
        >
          <Trash2 className="h-4 w-4" aria-hidden="true" />
          Hapus User
        </button>
      </div>

      {isCurrentAdmin ? (
        <div className="mt-5 rounded-lg bg-mint p-4 text-sm leading-6 text-ink/65">
          Ini akun yang sedang kamu pakai. Role admin akun sendiri tidak bisa dicabut dari halaman ini.
        </div>
      ) : null}
    </div>
  );
}

function DetailItem({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-lg bg-paper p-4">
      <dt className="text-xs font-semibold uppercase text-ink/50">{label}</dt>
      <dd className="mt-1 break-words text-sm font-semibold text-ink">{value || "-"}</dd>
    </div>
  );
}

function Metric({ label, value }: { label: string; value: number | string }) {
  return (
    <div className="rounded-lg bg-paper p-3">
      <p className="text-xs font-semibold uppercase text-ink/50">{label}</p>
      <p className="mt-1 font-semibold">{value}</p>
    </div>
  );
}

function StatusBadge({
  icon: Icon,
  label,
  tone
}: {
  icon: typeof MailCheck;
  label: string;
  tone: string;
}) {
  return (
    <span className={`inline-flex items-center gap-1 rounded-md px-2 py-1 text-xs font-semibold ${tone}`}>
      <Icon className="h-3.5 w-3.5" aria-hidden="true" />
      {label}
    </span>
  );
}
