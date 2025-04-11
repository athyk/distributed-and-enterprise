const base_url = 'http://localhost:8000/';
export async function get<T>(url: string, ignore: boolean = false, cred = true): Promise<T> {
	let formattedUrl = '';
	if (!ignore) {
		formattedUrl = base_url + url;
	} else {
		formattedUrl = url;
	}
	console.log('GET URL:', formattedUrl);
	try {
		const response = await fetch(formattedUrl, {
			method: 'GET',
			headers: {
				'Content-Type': 'application/json'
			},
			...(cred && { credentials: 'include' })
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
