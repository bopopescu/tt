package gen

import "lib/mapgen"

const world = `
01<>02<><><><><><><><><><><><><><><><><>
<><><><><><><><><><><><><><><><><><><><>
03<><><><><><><><><><><><><><><><><><><>
04<><><><><><><><><><><><><><><><><><><>
<><><><><><><><><><><><><><><><><><><><>
<><><><><><><><><><><><><><><><><><><><>
<><><><><><><><><><><><><><><><><><><><>
`

var M01 = mapgen.Area{
	Name: "Dragonclaw",
}

var M02 = mapgen.Area{
	Name: "Dragoncave",
}

var M03 = mapgen.Area{
	Name: "Twilight",
}

var M04 = mapgen.Area{
	Name: "Twilight Stables",
}
