"use client";

import { useEffect, useMemo, useState } from "react";
import { RefreshCcw, Search, ShieldCheck, ShieldMinus, ShieldPlus, UsersRound } from "lucide-react";
import type { AuthUser } from "@/lib/auth-api";
import { listAdminUsers, updateAdminUserRole, type AdminUser } from "@/lib/admin-users-api";

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

export function AdminUsersManager({ adminUser }: { adminUser: AuthUser }) {
  const [users, setUsers] = useState<AdminUser[]>([]);
  const [search, setSearch] = useState("");
  const [selectedUser, setSelectedUser] = useState<AdminUser | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [actionUserId, setActionUserId] = useState<string | null>(null);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    void loadUsers();
    // Load once when this admin screen opens.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const totals = useMemo(() => {
    return users.reduce(
      (acc, user) => {
        acc.count += 1;
        if (user.role === "admin") {
          acc.admin += 1;
        }
        return acc;
      },
      { admin: 0, count: 0 }
    );
  }, [users]);

  async function loadUsers(nextSearch = search) {
    setIsLoading(true);
    setMessage("");
    setError("");

    try {
      const nextUsers = await listAdminUsers({ search: nextSearch.trim(), limit: 200 });
      setUsers(nextUsers);
      setSelectedUser((current) => {
        if (!current) {
          return nextUsers[0] ?? null;
        }
        return nextUsers.find((user) => user.id === current.id) ?? nextUsers[0] ?? null;
      });
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
      setSelectedUser(updated);
      setMessage(role === "admin" ? `${updated.email} sekarang admin.` : `${updated.email} kembali menjadi student.`);
    } catch {
      setError("Role belum bisa diubah. Admin tidak bisa mencabut role admin dirinya sendiri.");
    } finally {
      setActionUserId(null);
    }
  }

  return (
    <div className="grid gap-5 lg:grid-cols-[0.36fr_0.64fr]">
      <section className="space-y-5">
        <div className="rounded-lg border border-ink/10 bg-white p-5 shadow-sm">
          <div className="flex items-start gap-3">
            <div className="grid h-10 w-10 place-items-center rounded-lg bg-mint">
              <UsersRound className="h-5 w-5 text-leaf" aria-hidden="true" />
            </div>
            <div>
              <p className="text-sm font-semibold uppercase text-leaf">Admin Users</p>
              <h1 className="mt-1 text-2xl font-semibold">User Access</h1>
              <p className="mt-2 text-sm leading-6 text-ink/60">
                Kelola role admin tanpa membuka database.
              </p>
            </div>
          </div>

          <div className="mt-5 rounded-lg bg-mint px-4 py-3 text-sm text-ink/70">
            Login sebagai <span className="font-semibold text-ink">{adminUser.email}</span>
          </div>
        </div>

        <div className="rounded-lg border border-ink/10 bg-white p-5 shadow-sm">
          <div className="flex items-center justify-between gap-3">
            <h2 className="font-semibold">Directory</h2>
            <button
              type="button"
              onClick={() => loadUsers()}
              disabled={isLoading}
              className="focus-ring inline-flex h-9 items-center justify-center gap-2 rounded-lg bg-ink px-3 text-sm font-semibold text-white disabled:cursor-not-allowed disabled:opacity-60"
            >
              <RefreshCcw className="h-4 w-4" aria-hidden="true" />
              Refresh
            </button>
          </div>

          <div className="mt-4 flex gap-2">
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
              placeholder="Cari email user"
            />
            <button
              type="button"
              onClick={() => loadUsers()}
              disabled={isLoading}
              className="focus-ring inline-flex h-10 w-10 items-center justify-center rounded-lg bg-mint text-leaf disabled:cursor-not-allowed disabled:opacity-60"
              aria-label="Cari user"
              title="Cari user"
            >
              <Search className="h-4 w-4" aria-hidden="true" />
            </button>
          </div>

          <div className="mt-4 grid grid-cols-2 gap-2 text-sm">
            <Metric label="Users" value={totals.count} />
            <Metric label="Admins" value={totals.admin} />
          </div>

          {message ? <p className="mt-4 rounded-lg bg-mint px-4 py-3 text-sm text-ink/70">{message}</p> : null}
          {error ? <p className="mt-4 rounded-lg bg-[#fde7df] px-4 py-3 text-sm text-ink/70">{error}</p> : null}
        </div>
      </section>

      <section className="grid gap-5 xl:grid-cols-[0.42fr_0.58fr]">
        <div className="rounded-lg border border-ink/10 bg-white p-5 shadow-sm">
          <h2 className="font-semibold">Users</h2>
          <div className="mt-4 space-y-3">
            {users.map((user) => (
              <button
                key={user.id}
                type="button"
                onClick={() => setSelectedUser(user)}
                className={`focus-ring w-full rounded-lg border p-4 text-left ${
                  selectedUser?.id === user.id ? "border-leaf bg-mint" : "border-ink/10 bg-paper hover:bg-mint"
                }`}
              >
                <div className="flex items-start justify-between gap-3">
                  <div className="min-w-0">
                    <p className="truncate font-semibold">{user.name || user.email}</p>
                    <p className="mt-1 truncate text-sm text-ink/60">{user.email}</p>
                  </div>
                  <span className={`rounded-md px-2 py-1 text-xs font-semibold ${roleTone(user.role)}`}>
                    {user.role}
                  </span>
                </div>
                <p className="mt-3 text-xs text-ink/50">Updated {formatDate(user.updatedAt)}</p>
              </button>
            ))}

            {!users.length ? (
              <div className="rounded-lg bg-paper p-5 text-sm leading-6 text-ink/60">
                Klik refresh atau cari email user.
              </div>
            ) : null}
          </div>
        </div>

        <div className="rounded-lg border border-ink/10 bg-white p-5 shadow-sm">
          {selectedUser ? (
            <UserDetail
              user={selectedUser}
              currentAdminId={adminUser.id}
              isActing={actionUserId === selectedUser.id}
              onPromote={() => updateRole(selectedUser, "admin")}
              onDemote={() => updateRole(selectedUser, "student")}
            />
          ) : (
            <div className="grid min-h-[360px] place-items-center rounded-lg bg-paper p-6 text-center">
              <div>
                <ShieldCheck className="mx-auto h-8 w-8 text-leaf" aria-hidden="true" />
                <h2 className="mt-4 text-xl font-semibold">Pilih user</h2>
                <p className="mt-2 text-sm leading-6 text-ink/60">
                  Detail role dan action admin akan muncul di sini.
                </p>
              </div>
            </div>
          )}
        </div>
      </section>
    </div>
  );
}

function UserDetail({
  user,
  currentAdminId,
  isActing,
  onPromote,
  onDemote
}: {
  user: AdminUser;
  currentAdminId: string;
  isActing: boolean;
  onPromote: () => void;
  onDemote: () => void;
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

      <dl className="mt-5 grid gap-3 md:grid-cols-2">
        <DetailItem label="User ID" value={user.id} />
        <DetailItem label="Email verified" value={formatDate(user.emailVerifiedAt)} />
        <DetailItem label="Created" value={formatDate(user.createdAt)} />
        <DetailItem label="Updated" value={formatDate(user.updatedAt)} />
      </dl>

      <div className="mt-5 grid gap-3 sm:grid-cols-2">
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
