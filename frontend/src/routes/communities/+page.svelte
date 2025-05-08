<script lang="ts">
	import CommunityCard from '$lib/components/communityCard/communityCard.svelte';
	import Sidebar from '$lib/components/communitySidebar/communitySidebar.svelte';
	import { get } from '$lib/api/get';
	import Popup from '$components/ErrorPopUp/popup.svelte';
	import type { CommunitySearchResponse, communityData } from '$lib/api/apiType';
	import CreateCommunityCard from '$components/communityCRUD/create.svelte';
	import { onMount } from 'svelte';
	import { isLoggedIn } from '$lib/api/checkUser';

	let tags: [string, number][] = [];
	let degree: [string, number][] = [];
	let modalShown = false;
	let ageTo: string = '';
	let is_with = 0;
	let public_community = 0;
	let isLoggedInUser = false;

	function removeTag(tag: [string, number]) {
		tags = tags.filter((t) => t[1] !== tag[1]);
	}

	function clearAllTags() {
		tags = [];
	}

	function buildQueryString() {
		let query = 'offset=0&limit=20&';

		if (tags.length > 0) {
			query += '&';
			query += tags.map((tag) => `tags=${tag[1]}`).join('&');
		}

		if (degree.length > 0) {
			query += '&';
			query += degree.map((deg) => `degrees=${deg[1]}`).join('&');
		}

		if (ageTo) {
			query += `&minimum_members=${ageTo}`;
		}

		if (is_with) {
			query += `&is_with=${is_with}`;
		}

		if (public_community) {
			query += `&public=${public_community}`;
		}

		if (searchQuery) {
			query += `&name=${searchQuery}`;
		}

		console.log(query);
		return query;
	}

	async function fetchCommunities() {
		isLoggedInUser = await isLoggedIn();
		console.log('User logged in:', isLoggedInUser);
		console.log('Fetching communities with query:', searchQuery);
		console.log(ageTo, is_with, public_community);
		error = '';

		const queryString = buildQueryString();

		try {
			const response = (await get('community/search?' + queryString)) as CommunitySearchResponse;
			console.log('Response:', response);
			filteredCommunities = response.communities || [];
		} catch (err) {
			error = 'Failed to fetch communities. Please try again later.';
			console.error('Error fetching communities:', err);
			return;
		}
	}

	$: if (
		tags.length > 0 ||
		searchQuery ||
		degree.length > 0 ||
		ageTo ||
		is_with ||
		public_community
	) {
		fetchCommunities();
	}

	let searchQuery: string = '';
	let filteredCommunities: communityData[] = [];
	let error: string = '';

	onMount(async () => {
		fetchCommunities();
	});
</script>

<!-- Component Layout (No changes needed here) -->
<Popup bind:errorMessage={error} />
<CreateCommunityCard bind:modalShown />
<div class="flex min-h-screen bg-gray-50">
	<!-- Sidebar Component -->
	<Sidebar bind:tags bind:degree bind:ageTo bind:is_with bind:public_community />
	<!-- Main Content -->
	<div class="ml-64 flex-1 p-6 pt-20">
		<div class="mx-auto max-w-6xl">
			<!-- Header with Search Bar and Create Community Button -->
			<div class="mb-8 flex flex-col items-center justify-between gap-4 sm:flex-row">
				<!-- Search Bar Section -->
				<!-- Header with Search Bar -->
				<div class="mb-8 flex flex-col items-center gap-4">
					<!-- Removed justify-between and sm:flex-row -->
					<!-- Search Bar Section -->
					<div
						class="flex w-full max-w-lg items-center gap-2 rounded-full border border-gray-300 bg-white p-2 px-3 shadow-sm focus-within:ring-2 focus-within:ring-blue-500 focus-within:ring-offset-1"
					>
						<svg
							xmlns="http://www.w3.org/2000/svg"
							class="h-5 w-5 text-gray-400"
							viewBox="0 0 20 20"
							fill="currentColor"
						>
							<path
								fill-rule="evenodd"
								d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z"
								clip-rule="evenodd"
							/>
						</svg>
						<input
							type="text"
							bind:value={searchQuery}
							placeholder="Search for a student..."
							class="w-full flex-1 bg-transparent px-2 text-gray-900 outline-none"
						/>
					</div>
				</div>

				<!-- Create Community Button -->
				{#if isLoggedInUser}
					<button
						class="flex shrink-0 items-center justify-center gap-2 rounded-lg bg-green-500 px-5 py-2.5 text-sm font-medium text-white shadow-md transition hover:bg-green-600 focus:ring-2 focus:ring-green-500 focus:ring-offset-2 focus:outline-none"
						on:click={() => (modalShown = true)}
					>
						<svg
							xmlns="http://www.w3.org/2000/svg"
							class="h-5 w-5"
							viewBox="0 0 20 20"
							fill="currentColor"
						>
							<path
								fill-rule="evenodd"
								d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z"
								clip-rule="evenodd"
							/>
						</svg>
						Create Community
					</button>
				{/if}
			</div>

			<!-- Active Filters Display -->
			{#if tags.length > 0}
				<div
					class="mb-6 flex flex-wrap items-center gap-2 rounded-lg border border-gray-200 bg-white p-3 shadow-sm"
				>
					<span class="text-sm font-medium text-gray-600">Active filters:</span>
					{#each tags as tag (tag[1])}
						<span
							class="inline-flex items-center rounded-full bg-blue-100 px-2.5 py-0.5 text-sm font-medium text-blue-800"
						>
							{tag[0]}
							<button
								class="-mr-1 ml-1.5 inline-flex flex-shrink-0 items-center justify-center rounded-full p-0.5 text-blue-500 hover:bg-blue-200 hover:text-blue-700 focus:bg-blue-200 focus:outline-none"
								aria-label={`Remove ${tag[0]} filter`}
								on:click={() => removeTag(tag)}
							>
								<svg class="h-2 w-2" stroke="currentColor" fill="none" viewBox="0 0 8 8">
									<path stroke-linecap="round" stroke-width="1.5" d="M1 1l6 6m0-6L1 7" />
								</svg>
							</button>
						</span>
					{/each}
					<button
						class="ml-auto pl-2 text-sm text-blue-600 hover:underline"
						on:click={clearAllTags}
					>
						Clear all
					</button>
				</div>
			{/if}

			<!-- Display Loading, Error, or Communities -->
			{#if filteredCommunities.length === 0}
				<!-- Show loading spinner only on initial load or when list is empty -->
				<div class="flex flex-col items-center justify-center py-12 text-center">
					<!-- Magnifying glass icon (Heroicons) - still appropriate for search -->
					<svg
						xmlns="http://www.w3.org/2000/svg"
						fill="none"
						viewBox="0 0 24 24"
						stroke-width="1.5"
						stroke="currentColor"
						class="mb-3 h-12 w-12 text-gray-400 dark:text-gray-500"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z"
						/>
					</svg>
					<p class="text-md font-medium text-gray-700 dark:text-gray-300">
						Ready to find a committee?
					</p>
					<p class="mt-1 text-sm text-gray-500 dark:text-gray-400">
						Enter a committee name or apply filters to see results.
					</p>
				</div>
			{:else if error}
				<div
					class="rounded-lg border border-red-200 bg-red-50 p-4 text-center text-red-700 shadow-sm"
				>
					<h3 class="font-medium">Oops! Something went wrong.</h3>
					<p class="mt-1 text-sm">{error}</p>
					<button
						on:click={() => fetchCommunities()}
						class="mt-3 inline-flex items-center rounded-md border border-transparent bg-red-100 px-3 py-1.5 text-sm font-medium text-red-700 hover:bg-red-200 focus:ring-2 focus:ring-red-500 focus:ring-offset-2 focus:ring-offset-red-50 focus:outline-none"
					>
						Try Again
					</button>
				</div>
			{:else if filteredCommunities.length > 0}
				<div class="grid w-full grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-3">
					{#each filteredCommunities as community (community.id)}
						<CommunityCard
							id={community.id}
							name={community.name}
							isPublic={community.public}
							description={community.description}
							tags={community.tags}
							degrees={community.degrees}
							totalMembers={community.member_count}
						/>
					{/each}
				</div>
			{:else}
				<!-- Improved "No Results" Message -->
				<div
					class="flex min-h-[200px] flex-col items-center justify-center rounded-lg border border-gray-200 bg-white p-8 text-center shadow-sm"
				>
					<svg
						class="mb-3 h-12 w-12 text-gray-400"
						fill="none"
						stroke="currentColor"
						viewBox="0 0 24 24"
						xmlns="http://www.w3.org/2000/svg"
						><path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0zM10 10a.01.01 0 01.01-.01M10 10a.01.01 0 00-.01-.01m.01.01H10m0 0v.01M10 10a.01.01 0 01.01.01m0 0a.01.01 0 00-.01.01m0-.01H10m0 0V9.99m0 .01a.01.01 0 00.01-.01m-.01.01H10m0 0V9.99"
						></path></svg
					>
					<h3 class="text-lg font-medium text-gray-800">No Communities Found</h3>
					<p class="mt-1 text-sm text-gray-500">
						{#if searchQuery || tags.length > 0}
							Try adjusting your search or filters.
						{:else}
							There are currently no communities listed. Why not create the first one?
						{/if}
					</p>
					{#if !searchQuery && tags.length === 0}
						<button
							class="mt-4 flex items-center justify-center gap-2 rounded-lg bg-green-500 px-4 py-2 text-sm font-medium text-white shadow-md transition hover:bg-green-600 focus:ring-2 focus:ring-green-500 focus:ring-offset-2 focus:outline-none"
						>
							<svg
								xmlns="http://www.w3.org/2000/svg"
								class="h-4 w-4"
								viewBox="0 0 20 20"
								fill="currentColor"
							>
								<path
									fill-rule="evenodd"
									d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z"
									clip-rule="evenodd"
								/>
							</svg>
							Create Community
						</button>
					{/if}
				</div>
			{/if}
		</div>
	</div>
</div>
