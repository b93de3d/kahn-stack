// dragHandle.svelte.js
// Action for marking an element as a drag handle

import { dragStore } from "./dragStore.svelte.js";

export function dragHandle(node) {
  function handleStart(e) {
    // Don't start drag if already dragging
    if (dragStore.dragging) return;

    // Prevent text selection
    e.preventDefault();

    // Signal that drag should start from this handle
    // The parent draggable action will handle the actual drag start
    const event = new CustomEvent("dragHandleDown", {
      bubbles: true,
      detail: { originalEvent: e },
    });
    node.dispatchEvent(event);
  }

  node.addEventListener("pointerdown", handleStart);
  node.style.cursor = "grab";
  node.style.touchAction = "none";

  return {
    destroy() {
      node.removeEventListener("pointerdown", handleStart);
    },
  };
}
