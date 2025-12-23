import type { ApiResponse } from 'apisauce';
import apiClient from './apiClient';


export enum DicketClientCurrency {
  EUR = 'EUR',
  GBP = 'GBP',
  USD = 'USD',
}

export enum DicketStatus {
  NOT_STARTED = 'NOT_STARTED',
  IN_PROGRESS = 'IN_PROGRESS',
  COMPLETE = 'COMPLETE',
}

export enum UpdateDicketStatus {
  NOT_STARTED = 'NOT_STARTED',
  IN_PROGRESS = 'IN_PROGRESS',
  COMPLETE = 'COMPLETE',
}

export enum ClientCurrency {
  EUR = 'EUR',
  GBP = 'GBP',
  USD = 'USD',
}

export enum CreateClientCurrency {
  EUR = 'EUR',
  GBP = 'GBP',
  USD = 'USD',
}

export enum TeamClientCurrency {
  EUR = 'EUR',
  GBP = 'GBP',
  USD = 'USD',
}

export enum RecurringDicketUnit {
  DAY = 'DAY',
  WEEK = 'WEEK',
  MONTH = 'MONTH',
  YEAR = 'YEAR',
}

export enum CreateRecurringDicketUnit {
  DAY = 'DAY',
  WEEK = 'WEEK',
  MONTH = 'MONTH',
  YEAR = 'YEAR',
}

export type ClientTeam = {
  name: string;
}

export type DicketClient = {
  uuid: string;
  name: string;
  rate: number;
  currency: DicketClientCurrency;
  teams: ClientTeam[];
}

export type UserProfile = {
  uuid: string;
  avatar: string | null;
  initials: string;
}

export type UserTeamUserProfile = {
  uuid: string;
  avatar: string | null;
  initials: string;
}

export type UserTeamUser = {
  profile: UserTeamUserProfile;
}

export type UserTeam = {
  name: string;
  users: UserTeamUser[];
}

export type User = {
  email: string;
  profile: UserProfile;
  teams: UserTeam[];
}

export type DicSessionDicket = {
  uuid: string;
}

export type DicSession = {
  uuid: string;
  start_time: string;
  duration: number | null;
  user: User;
  dicket: DicSessionDicket;
}

export type Comment = {
  uuid: string;
  posted: string;
  user: User;
  text: string;
}

export type Dicket = {
  uuid: string;
  client: DicketClient;
  title: string;
  created: string;
  status: DicketStatus;
  position: number;
  sessions: DicSession[];
  comments: Comment[];
  today: boolean;
  owner_profile: UserProfile;
}

export type CreateDicket = {
  title: string;
  client: string;
  today?: boolean;
}

export type UpdateDicket = {
  title?: string;
  created?: string;
  status?: UpdateDicketStatus;
  position?: number;
  client?: string;
  today?: boolean;
}

export type CreateDicSession = {
  hours: number | null;
  minutes: number | null;
  dicket: string | null;
}

export type UpdateDicSession = {
  start_time?: string;
  duration?: number | null;
  dicket_uuid?: string | null;
}

export type Client = {
  uuid: string;
  name: string;
  rate: number;
  currency: ClientCurrency;
  active_sessions: DicSession[];
  teams: ClientTeam[];
}

export type CreateClient = {
  name: string;
  rate: number;
  currency: CreateClientCurrency;
  teams: string[];
}

export type UpdateClient = {
  name: string;
}

export type TeamClient = {
  uuid: string;
  name: string;
  rate: number;
  currency: TeamClientCurrency;
}

export type Team = {
  uuid: string;
  name: string;
  owner: User;
  users: User[];
  clients: TeamClient[];
}

export type CreateTeam = {
  name: string;
}

export type RecurringDicket = {
  uuid: string;
  starting: string;
  until: string;
  interval: number;
  unit: RecurringDicketUnit;
  client: Client;
  title: string;
}

export type CreateRecurringDicket = {
  starting: string;
  until: string;
  interval: number;
  unit: CreateRecurringDicketUnit;
  title: string;
  client: string;
}

export type ApiToken = {
  token: string;
}

export type AddComment = {
  text: string;
}

export type TeamAddUser = {
  user: string;
}

const listDickets = (params: any): Promise<ApiResponse<{dickets: Dicket[]}>> =>
  apiClient.get(`/dickets/`, params)

const createDicket = (data: CreateDicket): Promise<ApiResponse<{dicket: Dicket}>> =>
  apiClient.post(`/dickets/`, data)

const deleteDicket = (uuid: any): Promise<ApiResponse<{dicket: Dicket}>> =>
  apiClient.delete(`/dickets/${uuid}/`)

const getDicket = (uuid: any): Promise<ApiResponse<{dicket: Dicket}>> =>
  apiClient.get(`/dickets/${uuid}/`)

const updateDicket = (uuid: any, data: UpdateDicket): Promise<ApiResponse<{dicket: Dicket}>> =>
  apiClient.patch(`/dickets/${uuid}/`, data)

const endSessionDicket = (uuid: any): Promise<ApiResponse<{dicket: Dicket}>> =>
  apiClient.get(`/dickets/${uuid}/end_session/`)

const startSessionDicket = (uuid: any): Promise<ApiResponse<{dicket: Dicket}>> =>
  apiClient.get(`/dickets/${uuid}/start_session/`)

const listDicSessions = (params: any): Promise<ApiResponse<{dic_sessions: DicSession[]}>> =>
  apiClient.get(`/sessions/`, params)

const createDicSession = (data: CreateDicSession): Promise<ApiResponse<{dic_session: DicSession}>> =>
  apiClient.post(`/sessions/`, data)

const deleteDicSession = (uuid: any): Promise<ApiResponse<{dic_session: DicSession}>> =>
  apiClient.delete(`/sessions/${uuid}/`)

const getDicSession = (uuid: any): Promise<ApiResponse<{dic_session: DicSession}>> =>
  apiClient.get(`/sessions/${uuid}/`)

const updateDicSession = (uuid: any, data: UpdateDicSession): Promise<ApiResponse<{dic_session: DicSession}>> =>
  apiClient.patch(`/sessions/${uuid}/`, data)

const endDicSession = (uuid: any): Promise<ApiResponse<{dic_session: DicSession}>> =>
  apiClient.get(`/sessions/${uuid}/end/`)

const listClients = (params: any): Promise<ApiResponse<{clients: Client[]}>> =>
  apiClient.get(`/clients/`, params)

const createClient = (data: CreateClient): Promise<ApiResponse<{client: Client}>> =>
  apiClient.post(`/clients/`, data)

const deleteClient = (uuid: any): Promise<ApiResponse<{client: Client}>> =>
  apiClient.delete(`/clients/${uuid}/`)

const getClient = (uuid: any): Promise<ApiResponse<{client: Client}>> =>
  apiClient.get(`/clients/${uuid}/`)

const updateClient = (uuid: any, data: UpdateClient): Promise<ApiResponse<{client: Client}>> =>
  apiClient.patch(`/clients/${uuid}/`, data)

const endSessionClient = (uuid: any): Promise<ApiResponse<{client: Client}>> =>
  apiClient.get(`/clients/${uuid}/end_session/`)

const startSessionClient = (uuid: any): Promise<ApiResponse<{client: Client}>> =>
  apiClient.get(`/clients/${uuid}/start_session/`)

const listTeams = (params: any): Promise<ApiResponse<{teams: Team[]}>> =>
  apiClient.get(`/teams/`, params)

const createTeam = (data: CreateTeam): Promise<ApiResponse<{team: Team}>> =>
  apiClient.post(`/teams/`, data)

const getTeam = (uuid: any): Promise<ApiResponse<{team: Team}>> =>
  apiClient.get(`/teams/${uuid}/`)

const listUsers = (params: any): Promise<ApiResponse<{users: User[]}>> =>
  apiClient.get(`/users/`, params)

const getCurrentDicketUser = (): Promise<ApiResponse<{dicket: Dicket}>> =>
  apiClient.get(`/users/get_current_dicket/`)

const listRecurringDickets = (params: any): Promise<ApiResponse<{recurring_dickets: RecurringDicket[]}>> =>
  apiClient.get(`/recurring_dickets/`, params)

const createRecurringDicket = (data: CreateRecurringDicket): Promise<ApiResponse<{recurring_dicket: RecurringDicket}>> =>
  apiClient.post(`/recurring_dickets/`, data)

const deleteRecurringDicket = (uuid: any): Promise<ApiResponse<{recurring_dicket: RecurringDicket}>> =>
  apiClient.delete(`/recurring_dickets/${uuid}/`)

const getApiTokenToken = (): Promise<ApiResponse<{token: ApiToken}>> =>
  apiClient.get(`/tokens/get_api_token/`)

const addCommentDicket = (uuid: any, data: AddComment): Promise<ApiResponse<{dicket: Dicket}>> =>
  apiClient.post(`/dickets/${uuid}/add_comment/`, data)

const addUserTeam = (uuid: any, data: TeamAddUser): Promise<ApiResponse<{team: Team}>> =>
  apiClient.post(`/teams/${uuid}/add_user/`, data)

const api = {
  listDickets,
  createDicket,
  deleteDicket,
  getDicket,
  updateDicket,
  endSessionDicket,
  startSessionDicket,
  listDicSessions,
  createDicSession,
  deleteDicSession,
  getDicSession,
  updateDicSession,
  endDicSession,
  listClients,
  createClient,
  deleteClient,
  getClient,
  updateClient,
  endSessionClient,
  startSessionClient,
  listTeams,
  createTeam,
  getTeam,
  listUsers,
  getCurrentDicketUser,
  listRecurringDickets,
  createRecurringDicket,
  deleteRecurringDicket,
  getApiTokenToken,
  addCommentDicket,
  addUserTeam,
}

export default api
