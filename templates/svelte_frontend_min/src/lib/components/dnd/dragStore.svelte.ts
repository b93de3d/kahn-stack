// dragStore.svelte.js
// Central store for managing drag state across all drag/drop actions

export const dragStore = $state({
  dragging: null,
  sourceContainer: null,
  sourceIndex: null,
  targetContainer: null,
  targetItemId: null, // ID of item we're hovering over
  insertBefore: true, // Insert before or after the target item
  ghostElement: null,
  offsetX: 0,
  offsetY: 0,
  isTouch: false,
});

export function startDrag(
  item,
  containerId,
  index,
  ghost,
  offsetX,
  offsetY,
  isTouch = false
) {
  dragStore.dragging = item;
  dragStore.sourceContainer = containerId;
  dragStore.sourceIndex = index;
  dragStore.targetContainer = containerId;
  // For touch: don't set targetItemId initially (no preview)
  // For mouse: set to item's own ID (preview in original position)
  dragStore.targetItemId = isTouch ? null : item.id || null;
  dragStore.insertBefore = true;
  dragStore.ghostElement = ghost;
  dragStore.offsetX = offsetX;
  dragStore.offsetY = offsetY;
  dragStore.isTouch = isTouch;
}

export function updateDragOver(containerId, targetItemId, insertBefore) {
  dragStore.targetContainer = containerId;
  dragStore.targetItemId = targetItemId;
  dragStore.insertBefore = insertBefore;
}

export function updateDragOverContainer(containerId) {
  dragStore.targetContainer = containerId;
  dragStore.targetItemId = null;
}

export function endDrag() {
  if (dragStore.ghostElement) {
    dragStore.ghostElement.remove();
  }

  const result = {
    item: dragStore.dragging,
    sourceContainer: dragStore.sourceContainer,
    sourceIndex: dragStore.sourceIndex,
    targetContainer: dragStore.targetContainer,
    targetItemId: dragStore.targetItemId,
    insertBefore: dragStore.insertBefore,
  };

  dragStore.dragging = null;
  dragStore.sourceContainer = null;
  dragStore.sourceIndex = null;
  dragStore.targetContainer = null;
  dragStore.targetItemId = null;
  dragStore.insertBefore = true;
  dragStore.ghostElement = null;
  dragStore.offsetX = 0;
  dragStore.offsetY = 0;
  dragStore.isTouch = false;

  return result;
}

export function isDragging(itemId) {
  return dragStore.dragging?.id === itemId;
}
