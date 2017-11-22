from io import StringIO
import ramlfications as r
import json


def raml_from_file(filepath):
    """
    Load RAML object from filepath.

    @param filepath string: RAML specs file path.
    """
    with open(filepath) as fp:
        return r.parse(fp)


def raml_from_string(ramlsource):
    """
    Load RAML object from string.
    @param ramlsource string: RAML specs string.

    returns 
    """
    sp = StringIO(ramlsource)
    tree = r.parse(sp)
    return tree


class SporeMethod:

    def __init__(self, name='', api_base_url='', method='', path='',
                 required_params=None, optional_params=None,
                 expected_status=None, required_payload=False, description='',
                 authentication=None, formats=None, base_url='',
                 documentation='', middlewares=None,
                 global_authentication=None, global_formats=None,
                 defaults=None):

        self.name = name
        self.path = path
        self.method = method
        self.required_params = required_params or []
        self.optional_params = optional_params or []
        self.required_payload = required_payload or []
        self.description = description
        self.documentation = documentation
        self.middlewares = middlewares or []
        self.formats = formats or []
        self.authentication = authentication or ""
        self.global_authentication = global_authentication
        self.global_formats = global_formats or []
        self.defaults = defaults
        self.form_data = {}
        self.media_type = ""

    def __str__(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class SporeFile:

    def __init__(self):
        self.baseuri = ""
        self.version = ""
        self.methods = {}
        self.authority = ""
        self.name = ""
        self.meta = {
            "documentation": ""
        }
        self.media_type = ""

    def __str__(self):
        # del d['raml_obj']
        return json.dumps(self, default=lambda o: {k: v for (k, v) in o.__dict__.items() if v},
                          sort_keys=True, indent=4)


def spore_from_raml_string(ramlsource):
    """
    Create SPORE from RAML specs.

    @param ramlsource str: RAML specs string.

    returns SPORE specs.
    """
    api = raml_from_string(ramlsource)
    spore_file = SporeFile()
    spore_file.baseuri = api.base_uri
    spore_file.version = api.version or ''
    spore_file.media_type = api.media_type

    for resource in api.resources:
        meth = SporeMethod()
        import ipdb
        ipdb.set_trace()
        meth.name = resource.raw['displayName']
        if resource.uri_params:
            meth.required_params = [
                param.name for param in resource.uri_params if param.required]
            meth.optional_params = [
                param.name for param in resource.uri_params if not param.required]
        meth.documentation = resource.desc
        meth.description = resource.desc
        meth.expected_status = [res.code for res in resource.responses]
        meth.payload = []
        try:
            if resource.body:
                meth.required_payload = list(resource.body[
                    0].raw['application/json']['properties'].keys())
        except:
            meth.required_payload = []
        meth.method = resource.method.upper()
        # meth.form_data = resource.form_data
        meth.media_type = resource.media_type
        spore_file.methods[meth.name] = meth
    return spore_file


def spore_from_raml_file(filepath):
    with open(filepath) as f:
        source = f.read()
        return spore_from_raml_string(source)
