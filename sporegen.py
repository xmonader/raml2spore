
import raml2spore

ramlfile = "todoapp.raml"

spore_file = raml2spore.spore_from_raml_file(ramlfile)
print(spore_file)
