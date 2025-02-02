export const BASE_URL = 'https://wado-backend-7f54306f53b0.herokuapp.com/api';

export function extractName(uri: string): string {
    return uri.includes('#') ? uri.split('#').pop()! : uri.split('/').pop()!;
}
