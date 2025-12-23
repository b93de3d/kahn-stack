<script>
  // DragItem.svelte
  // Helper component for individual draggable items with hover detection

  import { draggable } from "./draggable.svelte.js";
  import { dragStore, updateDragOver } from "./dragStore.svelte.js";

  let { item, containerId, index, children } = $props();

  let isDragging = $derived(dragStore.dragging?.id === item.id);

  function handlePointerMove(e) {
    if (!dragStore.dragging) return;
    if (isDragging) return;

    const rect = e.currentTarget.getBoundingClientRect();
    const midpoint = rect.top + rect.height / 2;
    const insertBefore = e.clientY < midpoint;

    updateDragOver(containerId, item.id, insertBefore);
  }
</script>

<div
  onpointermove={handlePointerMove}
  style:opacity={isDragging ? 0.5 : 1}
  style:transition="opacity 0.2s ease"
>
  <div
    use:draggable={{
      id: item.id,
      data: item,
      containerId,
      index,
    }}
  >
    {@render children()}
  </div>
</div>
