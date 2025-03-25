export type response = {
	success: boolean;
	error_message: string[];
	data: Record<string, unknown>;
};

export type RegiserResponse = {
	success: boolean;
	error_message: string[];
	user_id: number;
	otp_required: boolean;
};

export type PaginationData = {
	id: number;
	name: string;
	created_at: number;
	updated_at: number;
	count: number;
};

export type PaginationDataResponse = {
	http_status: number;
	success: boolean;
	error_message: string[];
	degrees: PaginationData[];
	tags: PaginationData[];
};
