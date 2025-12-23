<script>
  // Demo.svelte
  // Three-column kanban demo using the drag & drop actions

  import { dropzone } from "./dropzone.svelte.js";
  import { dragHandle } from "./dragHandle.svelte.js";
  import { dragStore } from "./dragStore.svelte.js";
  import DragItem from "./DragItem.svelte";

  let containers = $state({
    todo: [
      { id: "1", text: "Design mockups", type: "design" },
      { id: "2", text: "Write documentation", type: "docs" },
      { id: "3", text: "Code review PR #123", type: "code" },
    ],
    "in-progress": [
      { id: "4", text: "Implement drag & drop", type: "code" },
      { id: "5", text: "Update API endpoints", type: "code" },
    ],
    done: [
      { id: "6", text: "Setup project", type: "setup" },
      { id: "7", text: "Create wireframes", type: "design" },
    ],
  });

  // Compute the preview state based on target item, not indices
  let previewContainers = $derived.by(() => {
    if (!dragStore.dragging) return containers;

    const preview = {};
    const draggedItem = dragStore.dragging;

    // Copy all containers
    for (const [id, items] of Object.entries(containers)) {
      preview[id] = [...items];
    }

    // Remove dragged item from source
    preview[dragStore.sourceContainer] = preview[
      dragStore.sourceContainer
    ].filter((item) => item.id !== draggedItem.id);

    // Find where to insert in target
    const targetContainer = dragStore.targetContainer;
    const targetItems = preview[targetContainer];

    if (dragStore.targetItemId === null) {
      // No specific target, add to end
      preview[targetContainer] = [...targetItems, draggedItem];
    } else {
      // Insert before or after target item
      const targetIndex = targetItems.findIndex(
        (item) => item.id === dragStore.targetItemId
      );
      if (targetIndex !== -1) {
        const insertIndex = dragStore.insertBefore
          ? targetIndex
          : targetIndex + 1;
        preview[targetContainer] = [
          ...targetItems.slice(0, insertIndex),
          draggedItem,
          ...targetItems.slice(insertIndex),
        ];
      } else {
        // Target not found, add to end
        preview[targetContainer] = [...targetItems, draggedItem];
      }
    }

    return preview;
  });

  function handleDrop(result) {
    const {
      item,
      sourceContainer,
      targetContainer,
      targetItemId,
      insertBefore,
    } = result;

    // Remove from source
    containers[sourceContainer] = containers[sourceContainer].filter(
      (i) => i.id !== item.id
    );

    // Find insertion point in target
    const targetItems = containers[targetContainer];

    if (targetItemId === null) {
      // Add to end
      containers[targetContainer] = [...targetItems, item];
    } else {
      const targetIndex = targetItems.findIndex((i) => i.id === targetItemId);
      if (targetIndex !== -1) {
        const insertIndex = insertBefore ? targetIndex : targetIndex + 1;
        containers[targetContainer] = [
          ...targetItems.slice(0, insertIndex),
          item,
          ...targetItems.slice(insertIndex),
        ];
      } else {
        // Target not found, add to end
        containers[targetContainer] = [...targetItems, item];
      }
    }
  }

  const typeColors = {
    design: "background: #faf5ff; border-color: #e9d5ff;",
    docs: "background: #eff6ff; border-color: #bfdbfe;",
    code: "background: #f0fdf4; border-color: #bbf7d0;",
    setup: "background: #fff7ed; border-color: #fed7aa;",
  };
</script>

<div
  style="
  width: 100%;
  min-height: 100vh;
  background: linear-gradient(to bottom right, #f8fafc, #f1f5f9);
  padding: 2rem;
"
>
  <div style="max-width: 1200px; margin: 0 auto;">
    <div style="margin-bottom: 2rem;">
      <h1
        style="font-size: 1.875rem; font-weight: bold; color: #1e293b; margin-bottom: 0.5rem;"
      >
        Svelte 5 Drag & Drop
      </h1>
      <p style="color: #64748b;">
        Action-based architecture • Live preview while dragging
      </p>
    </div>

    <div
      style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.5rem;"
    >
      {#each Object.entries(previewContainers) as [containerId, items]}
        <div
          use:dropzone={{ id: containerId, onDrop: handleDrop }}
          style="
            background: white;
            border-radius: 0.5rem;
            box-shadow: 0 1px 2px rgba(0,0,0,0.05);
            border: 2px solid #e2e8f0;
            padding: 1rem;
            min-height: 400px;
          "
        >
          <h2
            style="
            font-size: 1.125rem;
            font-weight: 600;
            color: #334155;
            margin-bottom: 1rem;
            text-transform: capitalize;
          "
          >
            {containerId.replace("-", " ")}
            <span
              style="margin-left: 0.5rem; font-size: 0.875rem; color: #94a3b8;"
            >
              ({items.length})
            </span>
          </h2>

          <div style="display: flex; flex-direction: column; gap: 0.5rem;">
            {#each items as item (item.id)}
              {@const originalIndex = containers[containerId].findIndex(
                (i) => i.id === item.id
              )}
              <DragItem {item} {containerId} index={originalIndex}>
                <div
                  style="
                  border: 2px solid;
                  border-radius: 0.5rem;
                  padding: 0.75rem;
                  {typeColors[item.type]}
                "
                >
                  <div
                    style="display: flex; align-items: flex-start; gap: 0.75rem;"
                  >
                    <button
                      use:dragHandle
                      style="
                        margin-top: 0.125rem;
                        color: #94a3b8;
                        background: none;
                        border: none;
                        padding: 0;
                        cursor: grab;
                        transition: color 0.2s;
                      "
                      onmouseenter={(e) =>
                        (e.currentTarget.style.color = "#475569")}
                      onmouseleave={(e) =>
                        (e.currentTarget.style.color = "#94a3b8")}
                    >
                      <svg
                        width="16"
                        height="16"
                        viewBox="0 0 16 16"
                        fill="currentColor"
                      >
                        <circle cx="4" cy="3" r="1.5" />
                        <circle cx="4" cy="8" r="1.5" />
                        <circle cx="4" cy="13" r="1.5" />
                        <circle cx="12" cy="3" r="1.5" />
                        <circle cx="12" cy="8" r="1.5" />
                        <circle cx="12" cy="13" r="1.5" />
                      </svg>
                    </button>
                    <div style="flex: 1;">
                      <p style="color: #334155; font-weight: 500;">
                        {item.text}
                      </p>
                      <span
                        style="
                        font-size: 0.75rem;
                        color: #64748b;
                        margin-top: 0.25rem;
                        display: inline-block;
                      "
                      >
                        {item.type}
                      </span>
                    </div>
                  </div>
                </div>
              </DragItem>
            {/each}
          </div>
        </div>
      {/each}
    </div>

    <div
      style="
      margin-top: 2rem;
      padding: 1rem;
      background: #eff6ff;
      border: 1px solid #bfdbfe;
      border-radius: 0.5rem;
    "
    >
      <h3 style="font-weight: 600; color: #1e3a8a; margin-bottom: 0.5rem;">
        Implementation Notes:
      </h3>
      <ul
        style="font-size: 0.875rem; color: #1e40af; list-style: none; padding: 0;"
      >
        <li>
          • <strong>Live Preview</strong>
           - Items move to their new position as you drag
        </li>
        <li>
          • <strong>Opacity Feedback</strong>
           - Dragged item shows at 50% opacity
        </li>
        <li>
          • <strong>Commit on Release</strong>
           - Changes only saved when mouse is released
        </li>
        <li>
          • <strong>ID-based positioning</strong>
           - Tracks target item, not indices
        </li>
        <li>• Works within and between containers</li>
      </ul>
    </div>
  </div>
</div>
