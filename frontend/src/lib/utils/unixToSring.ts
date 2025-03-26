export function convertTimestamp(timestamp: string) {
	const date = new Date(parseInt(timestamp) * 1000);
	const options: Intl.DateTimeFormatOptions = {
		hour: 'numeric',
		minute: 'numeric',
		hour12: true,
		month: 'short',
		day: 'numeric',
		year: 'numeric'
	};
	const formattedDate = date.toLocaleString('en-GB', options);
	return formattedDate;
}
