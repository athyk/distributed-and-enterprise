<script lang="ts">
	// Data model for the form

	import { post } from '$lib/api/post';

	let formData = {
		name: '',
		description: '',
		public: false,
		tags: [] as number[],
		degrees: [] as string[]
	};

	type createResponse = {
		success: boolean;
		http_status: number;
		error_message: string[];
		id: number;
	};

	// Function to handle adding a tag
	function addTag() {
		const newTag = prompt('Enter a new tag');
		if (newTag) formData.tags = [...formData.tags, newTag];
	}

	// Function to handle removing a tag
	function removeTag(index: number) {
		formData.tags.splice(index, 1);
		formData.tags = [...formData.tags];
	}

	// Function to handle adding a degree
	function addDegree() {
		const newDegree = prompt('Enter a new degree');
		if (newDegree) formData.degrees = [...formData.degrees, newDegree];
	}

	// Function to handle removing a degree
	function removeDegree(index: number) {
		formData.degrees.splice(index, 1);
		formData.degrees = [...formData.degrees];
	}

	// Function to handle form submission
	async function createCommunity() {
		console.log('Creating community with data:', formData);

		try {
			let response = (await post('community/', formData)) as createResponse;

			console.log(response.id);
		} catch (error) {
			console.error('Error creating community:', error);
		}
	}

	// Add your API call or store logic here
</script>

<!-- Container -->
<div class="mx-auto max-w-xl rounded-md bg-gray-900 p-6 text-white shadow-md">
	<h1 class="mb-4 text-2xl font-bold">Create Community</h1>

	<!-- Name Field -->
	<div class="mb-4">
		<label for="communityName" class="mb-1 block text-sm font-medium">Name</label>
		<input
			id="communityName"
			type="text"
			bind:value={formData.name}
			class="w-full rounded-md border border-gray-700 bg-gray-800 p-2 focus:border-blue-500 focus:ring-blue-500"
		/>
	</div>

	<!-- Description Field -->
	<div class="mb-4">
		<label for="description" class="mb-1 block text-sm font-medium">Description</label>
		<textarea
			id="description"
			rows="3"
			bind:value={formData.description}
			class="w-full rounded-md border border-gray-700 bg-gray-800 p-2 focus:border-blue-500 focus:ring-blue-500"
		></textarea>
	</div>

	<!-- Public Checkbox -->
	<div class="mb-4 flex items-center">
		<input id="publicCheckbox" type="checkbox" bind:checked={formData.public} class="mr-2" />
		<label for="publicCheckbox" class="text-sm">Public</label>
	</div>

	<!-- Tags -->
	<div class="mb-4">
		<label for="tagInput" class="mb-1 block text-sm font-medium">Tags</label>
		<input id="tagInput" type="text" class="hidden" aria-hidden="true" />
		<div class="flex flex-wrap gap-2">
			{#each formData.tags as tag, index}
				<span class="flex items-center rounded-md border border-gray-700 bg-gray-800 px-2 py-1">
					{tag}
					<button
						type="button"
						class="ml-2 text-red-400 hover:text-red-600"
						on:click={() => removeTag(index)}
					>
						&times;
					</button>
				</span>
			{/each}
		</div>
		<button type="button" class="mt-1 text-sm text-blue-400 hover:text-blue-600" on:click={addTag}>
			+ Add Tag
		</button>
	</div>

	<!-- Degrees -->
	<div class="mb-4">
		<label for="degreeInput" class="mb-1 block text-sm font-medium">Degrees</label>
		<input id="degreeInput" type="text" class="hidden" aria-hidden="true" />
		<div class="flex flex-wrap gap-2">
			{#each formData.degrees as degree, index}
				<span class="flex items-center rounded-md border border-gray-700 bg-gray-800 px-2 py-1">
					{degree}
					<button
						type="button"
						class="ml-2 text-red-400 hover:text-red-600"
						on:click={() => removeDegree(index)}
					>
						&times;
					</button>
				</span>
			{/each}
		</div>
		<button
			type="button"
			class="mt-1 text-sm text-blue-400 hover:text-blue-600"
			on:click={addDegree}
		>
			+ Add Degree
		</button>
	</div>

	<!-- Create Button -->
	<button
		on:click={createCommunity}
		class="rounded-md bg-blue-600 px-4 py-2 font-semibold text-white hover:bg-blue-700"
	>
		Create Community
	</button>
</div>
