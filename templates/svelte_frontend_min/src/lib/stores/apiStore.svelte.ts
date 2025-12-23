import type { ApiResponse } from "apisauce";

export interface ApiState<T> {
  data: T;
  loading: boolean;
  error: string | null;
  lastUpdated: Date | null;
}

export function createApiStore<T>(
  apiFunc: (...args: any[]) => Promise<ApiResponse<T>>,
  defaultData: T,
  getArgs?: () => any[]
) {
  let state = $state<ApiState<T>>({
    data: defaultData,
    loading: false,
    error: null,
    lastUpdated: null,
  });

  const _fetch = async (...args: Parameters<typeof apiFunc>) => {
    state.loading = true;
    state.error = null;

    try {
      const response = await apiFunc(...args);
      state.data = response.ok && response.data ? response.data : defaultData;
      state.loading = false;
      state.error = response.ok ? null : JSON.stringify(response.data);
      state.lastUpdated = new Date();
      return response.data;
    } catch (error) {
      const errorMessage =
        error instanceof Error ? error.message : "An unknown error occurred";
      state.loading = false;
      state.error = errorMessage;
      throw error;
    }
  };

  const refresh = async (...args: Parameters<typeof apiFunc>) => {
    if (getArgs) {
      if (args.length > 0) {
        console.warn(
          "Args passed to createApiStore.refresh() when getArgs is set! This may become a hard error in futre."
        );
        console.warn("Args:", args);
      }
      return _fetch(...getArgs());
    }
    return _fetch(...args);
  };

  const reset = () => {
    state = {
      data: defaultData,
      loading: false,
      error: null,
      lastUpdated: null,
    };
  };

  if (getArgs) {
    $effect(() => {
      _fetch(...getArgs());
    });
  } else {
    _fetch();
  }

  return {
    get data() {
      return state.data;
    },
    get loading() {
      return state.loading;
    },
    get error() {
      return state.error;
    },
    get lastUpdated() {
      return state.lastUpdated;
    },
    fetch: refresh, // TODO: Rename fetch -> refresh everywhere
    reset,
  };
}
