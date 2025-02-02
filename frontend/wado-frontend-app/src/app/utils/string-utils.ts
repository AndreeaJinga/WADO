export function extractName(uri: string): string {
    return uri.includes('#') ? uri.split('#').pop()! : uri.split('/').pop()!;
}
