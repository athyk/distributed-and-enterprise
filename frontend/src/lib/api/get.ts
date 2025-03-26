const base_url = 'http://localhost:8000/';
export async function get<T>(url: string): Promise<T> {
	try {
		const response = await fetch(base_url + url, {
			method: 'GET',
			headers: {
				'Content-Type': 'application/json'
			},
			credentials: 'include'
		});

		const responseData = await response.json();

		if (!response.ok) {
			return responseData as T;
		}

		return responseData as T;
	} catch (error) {
		throw new Error('Failed to fetch: ' + error);
	}
}
