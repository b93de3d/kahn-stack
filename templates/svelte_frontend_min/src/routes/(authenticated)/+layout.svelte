<script lang="ts">
  import SignIn from "$lib/components/SignIn.svelte";
  import { globalDicket } from "$lib/stores/currentDicket.svelte";
  import { nav, ROUTES } from "$lib/stores/nav.svelte";
  import { userStore } from "$lib/stores/userStore.svelte";
  import { onDestroy, onMount } from "svelte";

  let { children } = $props();

  let loading = $state(true);

  const checkAuthenticated = async () => {
    await userStore.getSession();
    loading = false;
  };
  onMount(() => {
    checkAuthenticated();
    globalDicket.refreshCurrentDicket();
    const handleVisibilityChange = () => {
      if (document.visibilityState === "visible") {
        globalDicket.refreshCurrentDicket();
      }
    };
    document.addEventListener("visibilitychange", handleVisibilityChange);
    onDestroy(() => {
      document.removeEventListener("visibilitychange", handleVisibilityChange);
    });
  });

  let menuOpen = $state(false);
</script>

{#if loading}
  <div></div>
{:else if userStore.user !== null}
  <div class="layout">
    <div
      class="header"
      style={globalDicket.currentDicket
        ? "background-color: var(--green-4)"
        : ""}
    >
      <button
        class="navButton"
        onclick={() => {
          menuOpen = !menuOpen;
        }}
      >
        {menuOpen ? "ᚕ" : "ᚏ"}
      </button>
      {#if globalDicket.currentDicket}
        <a
          href={`/tickets/${globalDicket.currentDicket.uuid}`}
          style="color: var(--green-9);"
        >
          {globalDicket.currentDicket.title || "Untitled Dicket"}
        </a>
      {:else}
        <a href="/">_KAHN_PROJECT_TITLE_</a>
      {/if}
      <button class="navButton">?</button>
    </div>
    <div class="container">
      {#if menuOpen}
        <div class="menu">
          {#each ROUTES as route}
            <a
              href={route.path}
              onclick={() => {
                menuOpen = false;
              }}
              class={`navButton ${route.path === nav.activeRoute.path ? "active" : ""}`}
            >
              {route.title}
            </a>
          {/each}
          <button
            class="navButton"
            style="margin-top: auto;"
            onclick={userStore.logout}>ᚒ</button
          >
        </div>
      {/if}
      <div class="sidebar">
        {#each ROUTES as route}
          <a
            href={route.path}
            class={`navButton ${route.path === nav.activeRoute.path ? "active" : ""}`}
          >
            {route.icon}
          </a>
        {/each}
        <button
          class="navButton"
          style="margin-top: auto;"
          onclick={userStore.logout}>ᚒ</button
        >
      </div>
      <div class="main">
        {@render children()}
      </div>
    </div>
    <div class="mobileNav">
      {#each ROUTES as route}
        <a
          href={route.path}
          class={`navButton ${route.path === nav.activeRoute.path ? "active" : ""}`}
        >
          {route.icon}
        </a>
      {/each}
    </div>
  </div>
{:else}
  <SignIn />
{/if}

<style>
  .container {
    display: flex;
    flex-direction: row;
    height: calc(100dvh - 51px);
    position: relative;
  }
  .layout {
    display: flex;
    flex-direction: column;
  }
  .header {
    background-color: var(--dark-purple-7);
    border-bottom: 1px solid var(--purple-5);
    padding: 5px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    color: var(--purple-5);
    font-weight: 900;
    user-select: none;
    max-height: 51px;
  }
  .menu {
    position: absolute;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
    z-index: 99;
    background-color: var(--dark-purple-7);
    display: flex;
    flex-direction: column;
    padding: 5px;
    gap: 5px;
    max-width: 600px;
    border-right: 1px solid var(--purple-5);
  }
  .navButton {
    height: 40px;
    font-weight: bold;
  }
  .sidebar {
    width: 50px;
    background-color: var(--dark-purple-7);
    border-right: 1px solid var(--purple-5);
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 5px;
    gap: 5px;
  }
  .sidebar .navButton {
    width: 40px;
  }
  .header .navButton {
    width: 40px;
  }
  .main {
    position: relative;
    display: flex;
    flex-direction: row;
    flex: 1;
    overflow-y: auto;
  }
  .mobileNav {
    display: none;
    background-color: aqua;
    justify-content: space-around;
    padding: 5px;
    background-color: var(--dark-purple-7);
    border-top: 1px solid var(--purple-5);
    margin-top: 1px;
  }
  .mobileNav .navButton {
    width: 40px;
    height: 40px;
  }
  @media (max-width: 768px) {
    .mobileNav {
      display: flex;
    }
    .sidebar {
      display: none;
    }
    .container {
      height: calc(100dvh - 51px - 51px);
    }
  }
</style>
