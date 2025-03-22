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
};

export type PaginationDataResponse = {
	http_status: number;
	success: boolean;
	error_message: string[];
	degrees: PaginationData[];
	tags: PaginationData[];
};


export type globalAnnouncement = {
    "success": boolean,
    "http_status": number,
    "error_message": string[],
    "global_announcements": globalAnnouncementData[]
}


export type globalAnnouncementData = {
    "id": number,
    "title": string,
    "description": string,
    "tags": string[],
    "user_id": number,
    "uploaded": string,
    "edit_user_id": number,
    "edit_uploaded": string | null,
    "community_id": number,
}

export type postResponse = {
	"success": boolean,
	"error_message": string[],
	"posts": postsData[]
}

export type postsData = {
	"id": number,
	"title": string,
	"description": string,
	"tags": number[],
	"images" : string[],
	"user_id": number,
	"created_at": string,
	"updated_at": string,
}