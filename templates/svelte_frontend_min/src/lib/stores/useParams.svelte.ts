import { page } from "$app/state";
import { goto } from "$app/navigation";
import { addHours, format, parse } from "date-fns";

const DATE_FORMAT = "yyyy-MM-dd";

type PrimitiveTypes = "string" | "number" | "boolean" | "date";
type SupportedTypes = PrimitiveTypes | "string_array" | "date_array";

const _serializeDate = (v: any) => (v === null ? "" : format(v, DATE_FORMAT));
const _deserializeDate = (v: any) =>
  v === "" ? null : addHours(parse(v, DATE_FORMAT, new Date()), 12);

const serializers: Record<SupportedTypes, (value: any) => string> = {
  boolean: (v) => (v ? "true" : "false"),
  date: _serializeDate,
  number: (v) => v.toString(),
  string: (v) => (v === null ? "" : v),
  date_array: (v) => v.map(_serializeDate).join(","),
  string_array: (v) => v.join(",") || undefined,
};

const deserializers: Record<SupportedTypes, (value: string) => any> = {
  boolean: (v) => v === "true",
  date: _deserializeDate,
  number: (v) => parseFloat(v),
  string: (v) => (v === "" ? null : v),
  date_array: (v) => v.split(",").map(_deserializeDate),
  string_array: (v) => v.split(","),
};

function _isDate(value: any) {
  return value instanceof Date;
}

function _isDateOrNull(value: any) {
  if (value === null) return true;
  return _isDate(value);
}

const _getType = (value: any): SupportedTypes => {
  // _getType should only ever be called on developer specified objects
  // that will not change i.e. useParam initialValues.
  // This function is not safe to be called on runtime variables.
  if (Array.isArray(value)) {
    if (value.length === 2) {
      if (_isDateOrNull(value[0]) && _isDateOrNull(value[0]))
        return "date_array";
    }
    return "string_array";
  }
  if (value === "") {
    throw new Error(
      `useParams: Empty strings are not supported as default values. Please use null`
    );
  }
  if (value === null) return "string";
  if (typeof value === "string") return "string";
  if (typeof value === "boolean") return "boolean";
  if (typeof value === "number") return "number";
  if (_isDate(value)) return "date";

  throw new Error(`useParams: Unsupported Type: ${typeof value} ${value}`);
};

function getSerializedValues<Values>(
  typeMap: { [key: string]: SupportedTypes },
  formValues: Values
) {
  return Object.fromEntries(
    Object.entries(formValues as object).map(([key, value]) => [
      key,
      serializers[typeMap[key]](value),
    ])
  );
}

function getDeserializedValues(
  typeMap: { [key: string]: SupportedTypes },
  paramValues: URLSearchParams
) {
  return Object.fromEntries(
    paramValues
      .entries()
      .map(([key, value]) => [
        key,
        deserializers[typeMap[key]](value as string),
      ])
  );
}

function getInitialValues<Values>(
  query: URLSearchParams,
  defaultInitialValues: Values,
  typeMap: {
    [key: string]: SupportedTypes;
  }
): Values {
  const deserializedValues = getDeserializedValues(typeMap, query);
  const initialValues = { ...defaultInitialValues, ...deserializedValues };
  return initialValues;
}

type ParamConfig<T> = {
  defaultValues: T;
  resettable?: (keyof T)[];
};

type ParamStore<T> = {
  values: T;
};

export function useParams<T extends Record<string, any>>({
  defaultValues,
  resettable = [],
}: ParamConfig<T>) {
  const typeMap = Object.fromEntries(
    Object.entries(defaultValues as object).map(([key, value]) => [
      key,
      _getType(value),
    ])
  );

  let resets = Object.fromEntries(
    Object.entries(defaultValues).filter(([k, _]) => resettable.includes(k))
  );

  let paramStore: ParamStore<T> = $state(
    structuredClone({
      values: getInitialValues(
        page.url.searchParams || {},
        defaultValues,
        typeMap
      ),
    })
  );

  $inspect(paramStore);

  //   $inspect(params);
  //   $inspect(typeMap);

  function setParams(newValues: Partial<T>, reset = false) {
    paramStore.values = {
      ...paramStore.values,
      ...(reset ? resets : {}),
      ...newValues,
    };

    const url = new URL(page.url);

    const currentKeys = Array.from(url.searchParams.keys());
    currentKeys.forEach((k) => {
      url.searchParams.delete(k);
    });

    const serialized = getSerializedValues(typeMap, paramStore.values);

    Object.entries(serialized).forEach(([k, v]) => {
      if (v !== undefined) {
        url.searchParams.append(k, v);
      }
    });

    goto(url, {
      replaceState: true,
      noScroll: true,
      keepFocus: true,
    });
  }

  return {
    get params() {
      return paramStore.values;
    },
    setParams,
  };
}
