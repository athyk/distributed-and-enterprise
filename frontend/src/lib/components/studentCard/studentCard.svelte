<script lang="ts">
	// Props remain the same
	export let firstName: string;
	export let lastName: string;
	export let gender: string;
	export let dateOfBirth: string; // Prop is now used for calculation
	export let pictureUrl: string = '';
	export let degreeId: number;
	export let degreeName: string = 'Not specified';
	export let yearOfStudy: number;
	export let gradDate: string;
	export let tags: number[] = [];
	export let tagNames: string[] = [];

	// Helper to calculate age from date string
	function calculateAge(dobString: string): number | string {
		if (!dobString) return 'N/A'; // Handle empty or null dobString

		try {
			const birthDate = new Date(dobString);
			// Check if the parsed date is valid
			if (isNaN(birthDate.getTime())) {
				console.warn(`Invalid date format received for age calculation: ${dobString}`);
				return 'Invalid Date';
			}

			const today = new Date();
			let age = today.getFullYear() - birthDate.getFullYear();
			const monthDiff = today.getMonth() - birthDate.getMonth();

			// Adjust age if the birthday hasn't occurred yet this year
			if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
				age--;
			}

            // Return 0 if calculated age is negative (e.g., future date)
			return age < 0 ? 0 : age;

		} catch (e) {
			console.error('Error calculating age:', e);
			return 'Error'; // Indicate calculation error
		}
	}

    // Reactive declaration for age: Automatically updates when dateOfBirth changes
    $: age = calculateAge(dateOfBirth);

	// Helper to format other dates (like graduation)
	function formatDate(dateString: string): string {
		try {
			return new Date(dateString).toLocaleDateString();
		} catch (e) {
			return dateString; // Fallback
		}
	}
</script>

<!--
  Main container:
  - w-full: Takes full width of its parent container.
  - min-h-80: Ensures a minimum height for consistency (adjust value as needed).
  - Parent component should handle layout (e.g., CSS Grid) for multiple cards.
-->
<div class="flex w-full flex-col space-y-4 rounded-lg border border-gray-200 bg-white p-4 min-h-80">
	<!-- Header: Simplified, no bottom border -->
	<div class="flex items-center">
		{#if pictureUrl}
			<img src={pictureUrl} alt="Profile" class="mr-3 h-10 w-10 flex-shrink-0 rounded-full object-cover" />
		{:else}
			<!-- Lighter gray background for placeholder -->
			<div
				class="mr-3 flex h-10 w-10 flex-shrink-0 items-center justify-center rounded-full bg-gray-100 text-lg font-semibold text-gray-700"
			>
				{firstName.charAt(0)}{lastName.charAt(0)}
			</div>
		{/if}
		<!-- Name is already bold -->
		<h2 class="truncate text-xl font-bold text-gray-900">
			{firstName} {lastName}
		</h2>
		<!-- Connect button is removed -->
	</div>

	<!-- Student Info Grid: Labels medium, Data semibold -->
	<!-- Added Age field, calculated from dateOfBirth -->
	<div class="grid grid-cols-1 gap-x-4 gap-y-2 md:grid-cols-2">
		<div>
			<p class="text-sm font-medium text-gray-500">Gender</p>
			<p class="font-semibold text-gray-800">{gender}</p>
		</div>
		<div>
			<!-- New Age field -->
			<p class="text-sm font-medium text-gray-500">Age</p>
			<p class="font-semibold text-gray-800">{age}</p>
		</div>
		<div>
			<p class="text-sm font-medium text-gray-500">Degree</p>
			<p class="font-semibold text-gray-800">{degreeName}</p>
		</div>
		<div>
			<p class="text-sm font-medium text-gray-500">Year of Study</p>
			<p class="font-semibold text-gray-800">{yearOfStudy}</p>
		</div>
	</div>

	<!-- Expected Graduation: Label medium, Data semibold -->
	<div>
		<p class="text-sm font-medium text-gray-500">Expected Graduation</p>
		<p class="font-semibold text-gray-800">{formatDate(gradDate)}</p>
	</div>

	<!-- Tags/Interests: Label medium, Tags semibold, simpler style -->
	<!-- Using flex-grow to push the bottom row down if content is short -->
	{#if tagNames && tagNames.length > 0}
		<div class="flex-grow"> <!-- Make this section grow -->
			<p class="mb-1 text-sm font-medium text-gray-500">Interests</p>
			<div class="flex flex-wrap gap-2">
				{#each tagNames as tag}
					<!-- Lighter background, standard rounding, semibold text -->
					<span class="rounded-md bg-gray-100 px-2.5 py-0.5 text-sm font-semibold text-gray-800">
						{tag}
					</span>
				{/each}
			</div>
		</div>
    {:else}
        <!-- Add an empty growing div if there are no tags to ensure bottom row stays down -->
        <div class="flex-grow"></div>
	{/if}


	<!-- Bottom Row: Simplified, no top border -->
    <!-- This row will be pushed to the bottom because of flex-grow above -->
	<div class="mt-auto flex items-center justify-between pt-2 text-sm text-gray-600"> <!-- Added mt-auto and pt-2 for spacing -->
		<div class="flex items-center space-x-2">
			<!-- Year remains bold -->
			<span class="text-base font-bold text-gray-900">Year {yearOfStudy}</span>
			<span class="text-gray-500">Student</span>
		</div>
		<!-- Graduation year semibold -->
		<div class="font-semibold">
			Graduates in {new Date(gradDate).getFullYear()}
		</div>
	</div>
</div>