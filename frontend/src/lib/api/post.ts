const base_url = 'http://localhost:8000/';
export async function post<T>(url: string, data: Record<string, unknown>): Promise<T> {
	try {
		const response = await fetch(base_url + url, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(data)
		});

		if (!response.ok) {
			throw new Error(`Failed to fetch: ${response.status} ${response.statusText}`);
		}

		return response.json();
	} catch (error) {
		throw new Error('Failed to fetch' + error);
	}
}
