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
	success: boolean;
	http_status: number;
	error_message: string[];
	global_announcements: globalAnnouncementData[];
};

export type globalAnnouncementData = {
	id: number;
	title: string;
	description: string;
	tags: string[];
	user_id: number;
	uploaded: string;
	edit_user_id: number;
	edit_uploaded: string | null;
	community_id: number;
	user: UserInfo;
};

export type postResponse = {
	success: boolean;
	error_message: string[];
	posts: postsData[];
};

export type singlePostResponse = {
	success: boolean;
	error_message: string[];
	post: postsData;
};

export type singleAnnoucementResponse = {
	success: boolean;
	error_message: string[];
	announcement: globalAnnouncementData;
};

export type searchTagResponse = {
	success: boolean;
	error_message: string[];
	tag: {
		id: number;
		name: string;
		count: number;
		created_at: string;
		updated_at: string;
	};
};

export type postsData = {
	id: number;
	title: string;
	description: string;
	tags: string[];
	images: string[];
	user_id: number;
	user_data: UserInfo;
	created_at: string;
	updated_at: string;
};

export type UserInfo = {
	user_id: number;
	first_name: string;
	last_name: string;
	picture_url: string;
};

export type postCreateResponse = {
	success: boolean;
	post: postsData;
	error_message: string[];
};

export type ImageUploadResponse = {
	success: boolean;
	error: string[];
	file_url: string;
};

export type EventResponse = {
	success: boolean;
	error_message: string[];
	global_events: EventDataResponse[];
};

export type EventDataResponse = {
	id: number;
	community_id: number;
	title: string;
	description: string;
	location: string;
	datetime: string;
	duration: string;
	latitude: number;
	longitude: number;
	tags: string[];
};

export type MeResponse = {
	success: boolean;
	error_message: string[];
	user: {
		id: number;
		email: string;
		email_verified: number;
		first_name: string;
		last_name: string;
		gender: string;
		date_of_birth: string;
		picture_url: string;
		degree_id: number;
		year_of_study: number;
		grad_date: string;
		tags: number[];
		rank: string;
		created_at: string;
		updated_at: string;
	};
};

export type communityData = {
	id: number;
	name: string;
	description: string;
	public: boolean;
	tags: string[];
	degrees: string[];
	member_count: number;
};
export type CommunitySearchResponse = {
	success: boolean;
	error_message: string[];
	communities: communityData[];
};
