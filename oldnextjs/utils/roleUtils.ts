import { Role } from '../types/auth';

/**
 * Get the appropriate dashboard URL based on user role
 * @param role - User's role
 * @returns Dashboard URL path
 */
export const getDashboardUrl = (role: Role): string => {
  switch (role) {
    case Role.HOST:
      return '/hostdashboard';
    case Role.TRAVELER:
    case Role.EXPLORER:
    default:
      return '/dashboard';
  }
};

/**
 * Check if a role has host privileges
 * @param role - User's role
 * @returns Boolean indicating if user can host
 */
export const canHost = (role: Role): boolean => {
  return role === Role.HOST;
};

/**
 * Check if a role can book/explore tours
 * @param role - User's role
 * @returns Boolean indicating if user can book tours
 */
export const canExplore = (role: Role): boolean => {
  return [Role.TRAVELER, Role.EXPLORER, Role.HOST].includes(role);
};

/**
 * Get role display name
 * @param role - User's role
 * @returns Human-readable role name
 */
export const getRoleDisplayName = (role: Role): string => {
  switch (role) {
    case Role.HOST:
      return 'Host';
    case Role.TRAVELER:
      return 'Traveler';
    case Role.EXPLORER:
      return 'Explorer';
    default:
      return 'User';
  }
};
