import re
from typing import List

from rest_framework.schemas.generators import EndpointEnumerator
from rest_framework import serializers
from rest_framework.viewsets import GenericViewSet

from _KAHN_PROJECT_SLUG_.settings import PROJECT_ROOT
from tools.dynamic_rest.fields import DynamicRelationField
from tools.dynamic_rest.serializers import DynamicSerializer, DynamicListSerializer
from tools.dynamic_rest.viewsets import ViewSetReturnType


def lower_first(value: str):
    if len(value) == 0:
        return ""
    return f"{value[0].lower()}{value[1:]}"


def snake_to_camel(value: str):
    return value.title().replace("_", "")


class ActionConfig:
    def __init__(
        self,
        verb,
        action,
        path,
        view_set,
    ):
        vs_instance = view_set(action=action)
        serializer_class = vs_instance.get_serializer_class()
        supports_bulk = vs_instance.supports_bulk()
        return_type: ViewSetReturnType = vs_instance.get_return_type()
        self.verb = verb
        self.action = action
        self.supports_bulk = supports_bulk
        self.path = path
        self.serializer_class = serializer_class
        self.return_type = return_type
        self.name = view_set.serializer_class.get_name()
        self.plural_name = serializer_class.get_plural_name()

        self.title = snake_to_camel(self.name)
        self.plural_title = snake_to_camel(self.plural_name)

        if action == "list":
            self.many = True
            self.action_name = "list"
            self.data_param = "params"
            self.success_code = 200
        elif action == "retrieve":
            self.many = False
            self.action_name = "get"
            self.data_param = None
            self.success_code = 200
        elif action == "create":
            self.many = False
            self.action_name = "create"
            self.data_param = "data"
            self.success_code = 201
        elif action == "partial_update":
            self.many = "{" not in path
            self.action_name = "update"
            self.data_param = "data"
            self.success_code = 200
        elif action == "destroy":
            self.many = False
            self.action_name = "delete"
            self.data_param = None
            self.success_code = 204
        else:
            self.many = False
            self.action_name = action
            self.data_param = (
                None if serializer_class == view_set.serializer_class else "data"
            )
            self.success_code = 200
            # assert False, f"Unhandled action: {action}"

        self.action_title = lower_first(snake_to_camel(self.action_name))


class ApiSauceCodegen:

    def __init__(self):
        self.enums = {}
        self.types = {}
        self.api_methods = {}
        self.boilerplate_lines = [
            "import type { ApiResponse } from 'apisauce';\n"
            "import apiClient from './apiClient';\n"
            "\n\n"
        ]

    def _client_return_type(self, inner_type):
        return f"Promise<ApiResponse<{inner_type}>>"

    def _object_type(self, key, value):
        return f"{{{key}: {value}}}"

    def strip_repeated_words(self, text):
        words = re.findall("[A-Z][^A-Z]*", text)
        unique_words = [
            word for i, word in enumerate(words) if i == 0 or word != words[i - 1]
        ]
        return "".join(unique_words)

    def _get_field_type(self, field_name, field, type_name, config: ActionConfig):
        if isinstance(field, type) and issubclass(field, serializers.Serializer):
            field_type = str(field.__name__)
        elif isinstance(field, serializers.Serializer):
            field_type = str(field.__class__.__name__)
            self._add_serializer_type(field.__class__, config)
        elif isinstance(field, DynamicListSerializer):
            field_type = str(field.child.__class__.__name__) + "[]"
            self._add_serializer_type(field.child.__class__, config)
        elif isinstance(field, DynamicRelationField):
            # TODO: Inline embedded relationships
            field_type = str(field.serializer_class().__class__.__name__)
            self._add_serializer_type(field.serializer_class, config)
            if field.many:
                if field.embed or not field.read_only:
                    field_type += "[]"
                else:
                    field_type = f"({field_type} | int)[]"
            else:
                if not field.embed:
                    field_type += " | int"
        elif isinstance(field, serializers.ChoiceField):
            choices_name = snake_to_camel(field_name)
            if choices_name not in self.enums:
                enum_name = self.strip_repeated_words(type_name + choices_name)
                field_type = enum_name
                enum_inner = "\n".join(f"  {k} = '{k}'," for k in field.choices)
                enum_snippet = f"export enum {enum_name} {{\n" f"{enum_inner}\n" f"}};"
                self.enums[enum_name] = enum_snippet
            else:
                field_type = choices_name
        elif isinstance(field, serializers.CharField):
            field_type = "string"
        elif isinstance(field, serializers.IntegerField):
            field_type = "number"
        elif isinstance(field, serializers.FloatField):
            field_type = "number"
        elif isinstance(field, serializers.DecimalField):
            field_type = "number"
        elif isinstance(field, serializers.DateTimeField):
            field_type = "string"
        elif isinstance(field, serializers.DateField):
            field_type = "string"
        elif isinstance(field, serializers.BooleanField):
            field_type = "boolean"
        elif isinstance(field, serializers.UUIDField):
            field_type = "string"
        elif isinstance(field, serializers.PrimaryKeyRelatedField):
            field_type = "number"
        elif isinstance(field, serializers.ReadOnlyField):
            assert False, (
                f"{field_name}: cannot infer type of ReadOnlyField. "
                f"If possible, please use the relevant Field class with read_only=True"
            )
        elif isinstance(field, serializers.ImageField):
            field_type = "string"
        elif isinstance(field, serializers.FileField):
            field_type = "string" if config.verb in ["list", "get"] else "File"
        elif isinstance(field, serializers.JSONField):
            field_type = "unknown"
        elif isinstance(field, serializers.TimeField):
            field_type = "string"
        elif isinstance(field, serializers.URLField):
            field_type = "string"
        elif isinstance(field, serializers.SlugRelatedField):
            field_type = "string"
        elif isinstance(field, serializers.ManyRelatedField):
            if isinstance(field.child_relation, serializers.SlugRelatedField):
                field_type = "string[]"
            else:
                assert False, f"Unhandled ManyRelatedField field type: {field}"
        else:
            assert False, f"Unhandled field type: {field_name} {type(field)}"

        return field_type

    def _add_serializer_type(self, serializer_class, config):
        type_name = serializer_class.__name__

        serializer_instance = serializer_class()

        fields = serializer_instance.get_fields()

        type_inner = ""
        for field_name, field in fields.items():
            if isinstance(field, serializers.HiddenField):
                continue

            required = field.required
            allow_null = field.allow_null
            field_type = self._get_field_type(field_name, field, type_name, config)

            if allow_null:
                field_type = f"{field_type} | null"

            if not required:
                field_name = f"{field_name}?"

            type_inner += f"  {field_name}: {field_type};\n"

        type_inner = type_inner.rstrip("\n")
        type_snippet = f"export type {type_name} = {{\n" f"{type_inner}\n" f"}};"

        self.types[type_name] = type_snippet

    def gen_api_code(self, configs: List[ActionConfig]):
        for config in configs:

            path = config.path
            data_param = config.data_param
            args = []
            params = re.findall(r"\{(.+)}", config.path)
            if params:
                args += [(p, "any") for p in params]
                path = path.replace("{", "${")

            if data_param:
                if config.action in ["list", "retrieve"]:
                    args.append((data_param, "any"))
                elif config.supports_bulk:
                    args.append(
                        (
                            data_param,
                            f"{config.serializer_class.__name__} | {config.serializer_class.__name__}[]",
                        )
                    )
                else:
                    args.append((data_param, config.serializer_class.__name__))

            method_name = f"{config.action_title}{(config.plural_title if config.many else config.title)}"

            return_type_items = ";\n".join(
                f"  {item.item_key}: {(f'{self._get_field_type(None, item.item_type, None, config)}[]' if item.many else self._get_field_type(None, item.item_type, None, config))}"
                for item in config.return_type.items
            )

            return_type = self._client_return_type(f"{{\n{return_type_items}\n}}")

            args = ", ".join(f"{arg}: {t}" for arg, t in args)

            has_file_field = any(
                isinstance(
                    field,
                    serializers.FileField,
                )
                for field in config.serializer_class().get_fields().values()
            )
            if has_file_field and config.verb in ["post", "patch"]:
                lines = []
                lines.append(f"const {method_name} = ({args}): {return_type} => {{")
                lines.append(f"  const formData = new FormData();")
                lines.append(f"  if (Array.isArray(data)) {{")
                lines.append(f"    data.forEach((item, index) => {{")
                for field_name, field in config.serializer_class().get_fields().items():
                    lines.append(f"    if (item.{field_name} !== undefined) {{")
                    lines.append(
                        f"      formData.append(`{field_name}[${{index}}]`, item.{field_name});"
                    )
                    lines.append("    }")
                lines.append(f"  }});")
                lines.append(f"  }} else {{")
                for field_name, field in config.serializer_class().get_fields().items():
                    lines.append(f"    if (data.{field_name} !== undefined) {{")
                    if field.allow_null:
                        lines.append(
                            f"      formData.append('{field_name}', data.{field_name} || '');"
                        )
                    else:
                        lines.append(
                            f"      formData.append('{field_name}', data.{field_name});"
                        )
                    lines.append("    }")
                lines.append(f"  }}")
                lines.append(f"  return apiClient.{config.verb}(`{path}`, formData, {{")
                lines.append("    headers: { 'Content-Type': 'multipart/form-data' }")
                lines.append("  })")
                lines.append("}")
                self.api_methods[method_name] = "\n".join(lines)
            else:
                self.api_methods[method_name] = (
                    f"const {method_name} = ({args}): {return_type} =>"
                    f" apiClient.{config.verb}(`{path}`{f', {data_param}' if data_param else ''})"
                )

            self._add_serializer_type(config.serializer_class, config)


class RequestsCodegen:
    def __init__(self):
        self.enums = {}
        self.types = {}
        self.api_methods = {}
        with open("tools/eg_requests_client.py") as f:
            self.boilerplate_lines = f.readlines()

    def _client_return_type(self, inner_type):
        return f"Promise<ApiResponse<{inner_type}>>"

    def _object_type(self, key, value):
        return f"{{{key}: {value}}}"

    def strip_repeated_words(self, text):
        words = re.findall("[A-Z][^A-Z]*", text)
        unique_words = [
            word for i, word in enumerate(words) if i == 0 or word != words[i - 1]
        ]
        return "".join(unique_words)

    def _add_class(self, serializer_class):
        type_name = serializer_class.__name__

        serializer_instance = serializer_class()

        fields = serializer_instance.get_fields()

        init_args = ""
        init_body = ""
        for field_name, field in fields.items():
            required = field.required
            allow_null = field.allow_null
            if isinstance(field, DynamicRelationField):
                # TODO: Inline embedded relationships
                field_type = str(field.serializer_class().__class__.__name__)
                self._add_class(field.serializer_class)
                if field.many:
                    if field.embed or not field.read_only:
                        field_type = f"List[{field_type}]"
                    else:
                        field_type = f"List[{field_type} | int]"
                else:
                    if not field.embed:
                        field_type += " | int"
            elif isinstance(field, serializers.ChoiceField):
                choices_name = snake_to_camel(field_name)
                if choices_name not in self.enums:
                    enum_name = self.strip_repeated_words(type_name + choices_name)
                    field_type = enum_name
                    enum_inner = "\n".join(f'    {k} = "{k}"' for k in field.choices)
                    enum_snippet = f"class {enum_name}(Enum):\n" f"{enum_inner}\n"
                    self.enums[enum_name] = enum_snippet
                else:
                    field_type = choices_name
            elif isinstance(field, serializers.CharField):
                field_type = "str"
            elif isinstance(field, serializers.IntegerField):
                field_type = "int"
            elif isinstance(field, serializers.FloatField):
                field_type = "float"
            elif isinstance(field, serializers.DecimalField):
                field_type = "float"
            elif isinstance(field, serializers.DateTimeField):
                field_type = "datetime"
            elif isinstance(field, serializers.DateField):
                field_type = "date"
            elif isinstance(field, serializers.BooleanField):
                field_type = "bool"
            elif isinstance(field, serializers.UUIDField):
                field_type = "str"
            elif isinstance(field, serializers.PrimaryKeyRelatedField):
                field_type = "int"
            elif isinstance(field, serializers.ReadOnlyField):
                assert False, (
                    f"{field_name}: cannot infer type of ReadOnlyField. "
                    f"If possible, please use the relevant Field class with read_only=True"
                )
            elif isinstance(field, serializers.ImageField):
                field_type = "str"
            elif isinstance(field, serializers.FileField):
                field_type = "str"
            elif isinstance(field, serializers.JSONField):
                field_type = "unknown"
            elif isinstance(field, serializers.HiddenField):
                continue
            elif isinstance(field, serializers.TimeField):
                field_type = "str"
            elif isinstance(field, serializers.URLField):
                field_type = "str"
            elif isinstance(field, serializers.SlugRelatedField):
                field_type = "str"
            elif isinstance(field, serializers.ManyRelatedField):
                if isinstance(field.child_relation, serializers.SlugRelatedField):
                    field_type = "List[str]"
                else:
                    assert False, f"Unhandled ManyRelatedField field type: {field}"
            else:
                assert False, f"Unhandled field type: {field}"

            if allow_null:
                field_type = f"{field_type} | null"

            if not required:
                field_name = f"{field_name}?"

            init_args += f"        {field_name}: {field_type},\n"
            init_body += f"        self.{field_name} = {field_name}\n"

        init_args = init_args.rstrip("\n")
        type_snippet = (
            f"class {type_name}:\n"
            f"    def __init__(\n"
            f"        self,\n"
            f"{init_args}\n"
            f"    ):\n"
            f"{init_body}"
        )

        self.types[type_name] = type_snippet

    def gen_api_code(self, configs: List[ActionConfig]):
        for config in configs:
            path = config.path
            data_param = config.data_param
            args = []
            params = re.findall(r"\{(.+)}", config.path)
            if params:
                args += [(p, "str") for p in params]

            has_json_arg = False
            has_params_arg = False
            if data_param:
                if config.action in ["list", "retrieve"]:
                    args.append((data_param, "Dict"))
                    has_params_arg = True
                else:
                    args.append((data_param, config.serializer_class.__name__))
                    has_json_arg = True

            method_name = f"{config.action_title}_{(config.plural_name if config.many else config.name)}"

            return_type = f"List[{config.title}]" if config.many else config.title
            if config.verb == "delete":
                return_type = "None"

            args = ", ".join(f"{arg}: {t}" for arg, t in args)

            # code = (
            #     f"def {method_name}({args}) -> {return_type}:\n"
            #     f"    res = requests.{config.verb}(\n"
            #     f"        f'http://localhost:8000{path}',\n"
            #     f"{f'        json=serialize_object({data_param}, {config.serializer_class.__name__}),\n' if has_json_arg else ''}"
            #     f"{f'        params={data_param},\n' if has_params_arg else ''}"
            #     f"    )\n"
            #     f"    assert res.status_code == {config.success_code}, f'Error: {{res.text}}'\n"
            #
            # )
            code = ""

            if config.verb != "delete":
                code += (
                    f"    print(res.json())\n"
                    f"    return deserialize_res_data(res.json(), {return_type})\n"
                )

            self.api_methods[method_name] = code

            self._add_class(config.serializer_class)


def main():
    codegen = ApiSauceCodegen()

    unique_handlers = []
    endpoints = []
    for path, _, handler in EndpointEnumerator().get_api_endpoints():
        if handler not in unique_handlers:
            unique_handlers.append(handler)
            endpoints.append((path, handler))

    configs = []
    for path, handler in endpoints:
        if issubclass(handler.cls, GenericViewSet):
            view_set = handler.cls
            actions = getattr(handler, "actions")
            # print(view_set, path, actions)

            for verb, action in actions.items():
                if action == "list_related":
                    # Skip internal action (not exposed as an endpoint)
                    continue

                config = ActionConfig(
                    verb=verb,
                    action=action,
                    path=path,
                    view_set=view_set,
                )
                if config.action_name == "update" and config.many:
                    # Skip codegen for bulk patch
                    continue

                configs.append(config)

    codegen.gen_api_code(configs)

    output_lines = codegen.boilerplate_lines

    for k, v in codegen.enums.items():
        output_lines.append(v + "\n\n")

    for k, v in codegen.types.items():
        output_lines.append(v + "\n\n")

    for k, v in codegen.api_methods.items():
        output_lines.append(v + "\n\n")

    output_lines.append("const api = {\n")
    for k in codegen.api_methods.keys():
        output_lines.append(f"  {k},\n")
    output_lines.append("}\n\n")
    output_lines.append("export default api\n")

    for line in output_lines:
        print(line)

    for filepath in [
        PROJECT_ROOT / "ar_web/src/lib/api.ts",
    ]:
        with open(filepath, "w") as f:
            f.writelines(output_lines)


if __name__ == "__main__":
    main()
