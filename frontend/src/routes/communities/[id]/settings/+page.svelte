<script lang="ts">
	import { page } from '$app/stores';

	let activeTab: string = 'update';

	// Form data
	let formData = {
		name: '',
		description: '',
		public: false,
		tags: [] as number[],
		degrees: [] as string[]
	};

	let id: string;
	$: id = $page.params.id;

	// Function to add a new tag
	function addTag() {
		const newTag = prompt('Enter a new tag:');
		if (newTag) formData.tags = [...formData.tags, Number(newTag)];
	}

	// Function to remove a tag
	function removeTag(index: number) {
		formData.tags = formData.tags.filter((_, i) => i !== index);
	}

	// Function to add a new degree
	function addDegree() {
		const newDegree = prompt('Enter a new degree:');
		if (newDegree) formData.degrees = [...formData.degrees, newDegree];
	}

	// Function to remove a degree
	function removeDegree(index: number) {
		formData.degrees = formData.degrees.filter((_, i) => i !== index);
	}

	// Function to update the community (PUT request)
	async function updateCommunity() {
		console.log('Updating community with data:', formData);

		try {
			let response = await fetch(`/community/${id}`, {
				method: 'PUT',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify(formData)
			});

			if (!response.ok) {
				throw new Error('Failed to update community');
			}

			let data = await response.json();
			console.log(data.id);
		} catch (error) {
			console.error('Error updating community:', error);
		}
	}

	// Function to delete the community (DELETE request)
	async function deleteCommunity() {
		console.log('Deleting community...');

		try {
			let response = await fetch(`/community/${id}`, {
				method: 'DELETE'
			});

			if (!response.ok) {
				throw new Error('Failed to delete community');
			}

			console.log('Community deleted successfully');
		} catch (error) {
			console.error('Error deleting community:', error);
		}
	}
</script>

<!-- Main container -->
<div class="flex min-h-screen bg-gray-100 dark:bg-gray-900">
	<!-- Sidebar -->
	<aside class="w-64 border-r border-gray-200 bg-white p-4 dark:border-gray-700 dark:bg-gray-800">
		<h2 class="mb-4 text-lg font-bold text-gray-900 dark:text-gray-100">Community Settings</h2>
		<nav class="space-y-2">
			<button
				on:click={() => (activeTab = 'update')}
				class="w-full rounded-md px-3 py-2 text-left text-gray-800 transition hover:bg-gray-200 focus:outline-none dark:text-gray-200 dark:hover:bg-gray-700 {activeTab ===
				'update'
					? 'bg-gray-200 font-semibold dark:bg-gray-700'
					: ''}"
			>
				Update Community
			</button>
			<button
				on:click={() => (activeTab = 'delete')}
				class="w-full rounded-md px-3 py-2 text-left text-gray-800 transition hover:bg-gray-200 focus:outline-none dark:text-gray-200 dark:hover:bg-gray-700 {activeTab ===
				'delete'
					? 'bg-gray-200 font-semibold dark:bg-gray-700'
					: ''}"
			>
				Delete Community
			</button>
		</nav>
	</aside>

	<!-- Content Area -->
	<main class="flex-1 p-8">
		{#if activeTab === 'update'}
			<h1 class="mb-4 text-2xl font-bold text-gray-900 dark:text-gray-100">Update Community</h1>

			<div class="rounded-md bg-white p-4 shadow dark:bg-gray-800">
				<!-- Name -->
				<label for="name" class="block text-sm font-medium text-gray-700 dark:text-gray-300"
					>Name</label
				>
				<input
					id="name"
					type="text"
					bind:value={formData.name}
					class="mt-1 mb-3 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 dark:bg-gray-700 dark:text-gray-200"
				/>

				<!-- Description -->
				<label for="description" class="block text-sm font-medium text-gray-700 dark:text-gray-300"
					>Description</label
				>
				<textarea
					id="description"
					bind:value={formData.description}
					class="mt-1 mb-3 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 dark:bg-gray-700 dark:text-gray-200"
				></textarea>

				<!-- Public Toggle -->
				<div class="mb-3 flex items-center">
					<input id="public" type="checkbox" bind:checked={formData.public} class="mr-2" />
					<label for="public" class="text-sm font-medium text-gray-700 dark:text-gray-300"
						>Public</label
					>
				</div>

				<!-- Tags -->
				<div class="mb-3">
					<label
						for="tags-container"
						class="block text-sm font-medium text-gray-700 dark:text-gray-300">Tags</label
					>
					<div id="tags-container">
						{#each formData.tags as tag, i}
							<div class="mt-1 flex items-center">
								<span
									class="mr-2 rounded bg-gray-300 px-2 py-1 text-gray-900 dark:bg-gray-700 dark:text-gray-100"
									>{tag}</span
								>
								<button on:click={() => removeTag(i)} class="text-red-500 hover:text-red-700"
									>×</button
								>
							</div>
						{/each}
						<button on:click={addTag} class="mt-2 text-sm text-blue-600 hover:text-blue-800"
							>+ Add Tag</button
						>
					</div>
				</div>

				<!-- Degrees -->
				<div class="mb-3">
					<label
						for="degrees-container"
						class="block text-sm font-medium text-gray-700 dark:text-gray-300">Degrees</label
					>
					<div id="degrees-container">
						{#each formData.degrees as degree, i}
							<div class="mt-1 flex items-center">
								<span
									class="mr-2 rounded bg-gray-300 px-2 py-1 text-gray-900 dark:bg-gray-700 dark:text-gray-100"
									>{degree}</span
								>
								<button on:click={() => removeDegree(i)} class="text-red-500 hover:text-red-700"
									>×</button
								>
							</div>
						{/each}
						<button on:click={addDegree} class="mt-2 text-sm text-blue-600 hover:text-blue-800"
							>+ Add Degree</button
						>
					</div>
				</div>

				<button
					on:click={updateCommunity}
					class="rounded bg-blue-600 px-4 py-2 text-white transition hover:bg-blue-700"
				>
					Update Community
				</button>
			</div>
		{:else if activeTab === 'delete'}
			<h1 class="mb-4 text-2xl font-bold text-gray-900 dark:text-gray-100">Delete Community</h1>
			<p class="mb-4 text-gray-700 dark:text-gray-300">
				Permanently delete this community. This action cannot be undone.
			</p>
			<button
				on:click={deleteCommunity}
				class="rounded bg-red-600 px-4 py-2 text-white transition hover:bg-red-700"
			>
				Delete Community
			</button>
		{/if}
	</main>
</div>
