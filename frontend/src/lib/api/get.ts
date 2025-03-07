const base_url =  'http://localhost:8000/'
export async function get<T>(url: string): Promise<T> {
    try {
        const response = await fetch(base_url+url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        });

        if (!response.ok) {
            throw new Error(`Failed to fetch: ${response.status} ${response.statusText}`);
        }

        return response.json();
    }
    catch (error) {
        throw new Error('Failed to fetch: ' + error);
    }
}