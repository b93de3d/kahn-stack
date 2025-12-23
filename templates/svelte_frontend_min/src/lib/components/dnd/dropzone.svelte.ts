// dropzone.svelte.js
// Action for marking an element as a drop zone

import {
  dragStore,
  updateDragOverContainer,
  endDrag,
} from "./dragStore.svelte.js";

export function dropzone(node, params) {
  let { id, onDrop } = $derived(params);

  function handlePointerEnter() {
    if (!dragStore.dragging) return;
    updateDragOverContainer(id);
  }

  function handleEnd() {
    if (!dragStore.dragging) return;

    const result = endDrag();
    document.body.style.cursor = "";

    if (onDrop && result.item) {
      onDrop(result);
    }
  }

  node.addEventListener("pointerenter", handlePointerEnter);

  const endCleanup = $effect.root(() => {
    window.addEventListener("pointerup", handleEnd);
    window.addEventListener("pointercancel", handleEnd);
    return () => {
      window.removeEventListener("pointerup", handleEnd);
      window.removeEventListener("pointercancel", handleEnd);
    };
  });

  return {
    destroy() {
      node.removeEventListener("pointerenter", handlePointerEnter);
      endCleanup();
    },
  };
}
