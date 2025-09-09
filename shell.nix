{ pkgs ? import <nixpkgs> { } }:

let
  projectRoot = toString ./.;
  cargoHome = "${projectRoot}/tools/projects/.cargo";
  cargoTarget = "${projectRoot}/tools/projects/target";
in

with pkgs;

mkShell rec {
  buildInputs = [
    pkg-config
    uv
    openssl
  ];

  LD_LIBRARY_PATH = lib.makeLibraryPath buildInputs;

  CARGO_TARGET_DIR = cargoTarget;
  CARGO_INCREMENTAl= "1";
  RUST_BACKTRACE = "1";

  CARGO_HOME = cargoHome;
  CARGO_NET_OFFLINE = "false";

  CARGO_BUILD_JOBS = toString (lib.min 16 (lib.max 1 pkgs.stdenv.hostPlatform.parsed.cpu.cores or 8));

  shellHook = ''
    mkdir -p "${cargoHome}"
    mkdir -p "${cargoTarget}"

    cat > "${cargoHome}/config.toml" << EOF
[build]
jobs = $CARGO_BUILD_JOBS
incremental = true

[env]
PKG_CONFIG_PATH = "${lib.makeSearchPath "lib/pkgconfig" buildInputs}"
EOF
  '';
}
