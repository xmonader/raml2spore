
import raml2spore

ramlfile = "todoapp.raml"

spore_file = raml2spore.spore_from_raml_file(ramlfile)
with open("todoapi.json", "w") as f:
    f.write(str(spore_file))
