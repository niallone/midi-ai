/**
 * Formats a duration in seconds to a string in the format "MM:SS"
 * 
 * @param {number} seconds - The duration in seconds
 * @returns {string} The formatted duration string
 */
export function formatDuration(seconds) {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = Math.floor(seconds % 60);
    return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
}