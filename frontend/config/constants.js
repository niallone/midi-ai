/**
 * Application-wide constants
 */

/**
 * The name of the application.
 * Used in various places throughout the UI for consistent branding.
 */
export const APP_NAME = 'AI Melody Generator';

/**
 * The base URL for API requests.
 * In development, it points to the local backend server.
 * In production, it should be updated to point to the deployed API endpoint.
 */
export const API_BASE_URL = 'http://localhost:4050'; //'https://api.melodygenerator.fun' ||

/**
 * The maximum length of generated melodies in seconds.
 * This constant is used to limit the duration of generated melodies
 * to ensure reasonable file sizes and generation times.
 */
export const MAX_MELODY_LENGTH = 60;