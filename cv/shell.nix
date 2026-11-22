{ pkgs ? import <nixpkgs> { config.allowUnfree = true; } }:
let
  pythonEnv = pkgs.python3.withPackages (ps: with ps; [
    unidecode
    tqdm
    pyyaml
    ruamel-yaml
    requests
    lxml
    playwright
  ]);
in
  pkgs.mkShell {
    nativeBuildInputs = with pkgs; [
      playwright-driver.browsers
      pythonEnv
    ];

    shellHook = ''
      export PLAYWRIGHT_BROWSERS_PATH=${pkgs.playwright-driver.browsers}
      export PLAYWRIGHT_SKIP_VALIDATE_HOST_REQUIREMENTS=true
      export PLAYWRIGHT_HOST_PLATFORM_OVERRIDE="ubuntu-24.04"
    '';
  }
