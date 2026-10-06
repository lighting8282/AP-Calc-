// Run inside the AP Calc Unity project (unity command eval_file ... --file this)
// to write the game's own item and location tables to
// apcalc/test/unity_tables.json. test_data compares data.py against it, so the
// world and the game can't drift apart unnoticed. Re-run after changing
// APItems.cs or APLocations.cs.
var items = new System.Text.StringBuilder();
foreach (var it in APItems.All)
    items.Append($"    {{\"name\": {Json(it.name)}, \"id\": {it.id}, \"kind\": \"{it.kind}\"}},\n");
var locs = new System.Text.StringBuilder();
for (int n = 1; n <= APLocations.MaxEquations; n++)
    locs.Append($"    {{\"name\": {Json(APLocations.EquationName(n))}, \"id\": {APLocations.EquationId(n)}}},\n");
foreach (var k in APLocations.Keys)
    locs.Append($"    {{\"name\": {Json(k.Location)}, \"id\": {k.id}, \"tier\": \"{APItems.TierOf(k.symbol)}\"}},\n");
foreach (APLocations.PowerUp p in System.Enum.GetValues(typeof(APLocations.PowerUp)))
    locs.Append($"    {{\"name\": {Json(APLocations.Name(p))}, \"id\": {APLocations.Id(p)}}},\n");
foreach (int n in APLocations.FunnyNumbers)
    locs.Append($"    {{\"name\": {Json(APLocations.FunnyName(n))}, \"id\": {APLocations.FunnyId(n)}}},\n");
string json = "{\n  \"items\": [\n" + items.ToString().TrimEnd(',', '\n') + "\n  ],\n  \"locations\": [\n" +
              locs.ToString().TrimEnd(',', '\n') + "\n  ]\n}\n";
string path = @"A:\Archipelago\Games\AP Calc\apcalc\test\unity_tables.json";
System.IO.Directory.CreateDirectory(System.IO.Path.GetDirectoryName(path));
System.IO.File.WriteAllText(path, json, new System.Text.UTF8Encoding(false));
return $"wrote {APItems.All.Count} items, {APLocations.MaxEquations + APLocations.Keys.Count + 3 + APLocations.FunnyNumbers.Length} locations";

string Json(string s) => "\"" + s.Replace("\\", "\\\\").Replace("\"", "\\\"") + "\"";
