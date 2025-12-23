// draggable.svelte.js
// Action for making an element draggable using Pointer Events

import { dragStore, startDrag } from "./dragStore.svelte.js";

export function draggable(node, params) {
  let { id, data, containerId, index } = $derived(params);
  let autoScrollInterval = null;

  // Find scrollable parent
  function findScrollableParent(element) {
    let parent = element.parentElement;
    while (parent) {
      const overflow = window.getComputedStyle(parent).overflowY;
      if (
        (overflow === "auto" || overflow === "scroll") &&
        parent.scrollHeight > parent.clientHeight
      ) {
        return parent;
      }
      parent = parent.parentElement;
    }
    return null;
  }

  // Auto-scroll when near edges
  function handleAutoScroll(clientY) {
    const scrollable = findScrollableParent(node);
    if (!scrollable) return;

    const rect = scrollable.getBoundingClientRect();
    const scrollZone = 50;
    const scrollSpeed = 10;

    const distanceFromTop = clientY - rect.top;
    const distanceFromBottom = rect.bottom - clientY;

    if (autoScrollInterval) {
      clearInterval(autoScrollInterval);
      autoScrollInterval = null;
    }

    if (distanceFromTop < scrollZone && distanceFromTop > 0) {
      autoScrollInterval = setInterval(() => {
        scrollable.scrollTop -= scrollSpeed;
      }, 16);
    } else if (distanceFromBottom < scrollZone && distanceFromBottom > 0) {
      autoScrollInterval = setInterval(() => {
        scrollable.scrollTop += scrollSpeed;
      }, 16);
    }
  }

  function handleDragHandleDown(e) {
    const originalEvent = e.detail.originalEvent;
    const clientX = originalEvent.clientX;
    const clientY = originalEvent.clientY;

    const isTouch = originalEvent.pointerType === "touch";

    // Get dimensions and position
    const rect = node.getBoundingClientRect();
    const offsetX = clientX - rect.left;
    const offsetY = clientY - rect.top;

    // Create ghost element
    const ghost = node.cloneNode(true);
    ghost.style.position = "fixed";
    ghost.style.pointerEvents = "none";
    ghost.style.opacity = "0.8";
    ghost.style.zIndex = "1000";
    ghost.style.width = rect.width + "px";
    ghost.style.left = clientX - offsetX + "px";
    ghost.style.top = clientY - offsetY + "px";
    ghost.style.transform = "rotate(3deg)";
    ghost.style.boxShadow = "0 10px 30px rgba(0,0,0,0.3)";
    document.body.appendChild(ghost);

    // Start drag - pass isTouch flag
    startDrag(data, containerId, index, ghost, offsetX, offsetY, isTouch);

    document.body.style.cursor = "grabbing";
  }

  function handleMove(e) {
    if (!dragStore.ghostElement) return;

    const clientX = e.clientX;
    const clientY = e.clientY;

    dragStore.ghostElement.style.left = clientX - dragStore.offsetX + "px";
    dragStore.ghostElement.style.top = clientY - dragStore.offsetY + "px";

    handleAutoScroll(clientY);
  }

  function handleEnd() {
    if (autoScrollInterval) {
      clearInterval(autoScrollInterval);
      autoScrollInterval = null;
    }
  }

  // Listen for drag handle events
  node.addEventListener("dragHandleDown", handleDragHandleDown);

  // Global pointer move/up for dragging
  const cleanup = $effect.root(() => {
    window.addEventListener("pointermove", handleMove);
    window.addEventListener("pointerup", handleEnd);
    window.addEventListener("pointercancel", handleEnd);
    return () => {
      window.removeEventListener("pointermove", handleMove);
      window.removeEventListener("pointerup", handleEnd);
      window.removeEventListener("pointercancel", handleEnd);
    };
  });

  return {
    destroy() {
      node.removeEventListener("dragHandleDown", handleDragHandleDown);
      if (autoScrollInterval) {
        clearInterval(autoScrollInterval);
      }
      cleanup();
      document.body.style.cursor = "";
    },
  };
}
