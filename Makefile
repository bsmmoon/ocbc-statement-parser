hello:
	echo "hello world!"

shell:
	nix-shell -p "python3.withPackages(ps: [ ps.pypdf ])"

run:
	nix-shell -p "python3.withPackages(ps: [ ps.pypdf ])" --run "python3 main.py" --pure
