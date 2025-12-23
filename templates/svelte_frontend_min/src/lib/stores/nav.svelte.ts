export enum Route {
  CLIENTS = "CLIENTS",
  TICKETS = "TICKETS",
  SESSIONS = "SESSIONS",
  TEAMS = "TEAMS",
  ACCOUNT = "ACCOUNT",
}

type RouteDetail = {
  title: string;
  path: string;
  icon: string;
};

export const ROUTE_DETAILS: Record<Route, RouteDetail> = {
  TICKETS: {
    icon: "D",
    path: "/",
    title: "Tickets",
  },
  CLIENTS: {
    icon: "C",
    path: "/clients",
    title: "Clients",
  },
  SESSIONS: {
    icon: "S",
    path: "/sessions",
    title: "Sessions",
  },
  TEAMS: {
    icon: "T",
    path: "/teams",
    title: "Teams",
  },
  ACCOUNT: {
    icon: "A",
    path: "/account",
    title: "Account",
  },
};

export const ROUTES = Object.values(ROUTE_DETAILS);

const HOME_ROUTE = Route.CLIENTS;

export function createNavigationState() {
  let activeRoute = $state(ROUTE_DETAILS[HOME_ROUTE]);

  return {
    get activeRoute() {
      return activeRoute;
    },
    setRoute(route: Route) {
      activeRoute = ROUTE_DETAILS[route];
    },
  };
}

export const nav = createNavigationState();
