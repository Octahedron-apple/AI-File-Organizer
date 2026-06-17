{ pkgs ? import <nixpkgs> {} }:

let
  python = pkgs.python3.withPackages (ps: [ ps.tkinter ps.pip ]);
in
pkgs.mkShell {
  buildInputs = [ python ];

  shellHook = ''
    export PIP_PREFIX="$(pwd)/.pip_packages"
    export PYTHONPATH="$PIP_PREFIX/lib/python${pkgs.python3.pythonVersion}/site-packages:$PYTHONPATH"
    export PATH="$PIP_PREFIX/bin:$PATH"
    mkdir -p "$PIP_PREFIX"

    if [ ! -f "$PIP_PREFIX/.installed" ]; then
      echo "Installing pip dependencies..."
      pip install --prefix="$PIP_PREFIX" -r requirements.txt -q
      touch "$PIP_PREFIX/.installed"
    fi

    echo "Environment ready! Run: python main.py"
  '';
}
