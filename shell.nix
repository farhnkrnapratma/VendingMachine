{
	pkgs ? import <nixpkgs> { },
}:

pkgs.mkShell {
	name = "BobaMachine Nix";
	buildInputs = with pkgs; [
		python315
		bun
		uv
		neovim
	];
}
