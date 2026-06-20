export const ASSET_VERSION = "v2.4";

export function versionedAssetSrc(src: string) {
  const separator = src.includes("?") ? "&" : "?";
  return `${src}${separator}v=${encodeURIComponent(ASSET_VERSION)}`;
}
