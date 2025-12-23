<script lang="ts">
  import api, { DicketStatus } from "$lib/api";
  import SortableTickets from "$lib/components/SortableTickets.svelte";
  import { nav, Route } from "$lib/stores/nav.svelte";
  import { createApiStore } from "$lib/stores/newApiStore.svelte";

  nav.setRoute(Route.TICKETS);

  const ticketsStore = createApiStore(
    () =>
      api.listDickets({
        "filter{-status}": DicketStatus.COMPLETE,
      }),
    { dickets: [] }
  );

  const clientsStore = createApiStore(api.listClients, {
    clients: [],
  });
</script>

<div class="container">
  <SortableTickets
    dickets={ticketsStore.data.dickets}
    refreshDickets={ticketsStore.fetch}
    clients={clientsStore.data.clients}
  />
</div>

<style>
  .container {
    flex: 1;
    display: flex;
    flex-direction: column;
    margin: var(--spacing-md);
    gap: var(--spacing-md);
  }
</style>
