<script lang="ts">
	export let eventTitle: string = 'Event Title';
	export let description: string =
		'Event Desc Event Desc Event Desc Event Desc Event Desc Event Desc Event Desc Event Desc Event Desc Event Desc Event Desc Event Desc Event Desc Event Desc Event Desc Event Desc Event Desc Event Desc Event Desc Event Desc Event Desc Event Desc Event Desc Event Desc Event Desc Event Desc';
	export let hostedBy: string = 'Hosted by X Community';
	export let eventDate: string = 'Event Date';
	export let eventTags: string = 'Event Tags';
	export let eventTime: string = 'Event Time Duration';
	export let eventLocation: string = 'Event Location';
	export let attendees: string = 'Number of Attendees';
</script>

<div class="mx-auto w-full max-w-2xl rounded-2xl bg-white p-6 shadow-lg dark:bg-gray-900">
	<!-- Event Title -->
	<h1 class="mb-4 text-center text-2xl font-bold text-gray-900 dark:text-white">
		{eventTitle}
	</h1>

	<!-- Event Description -->
	<p class="mb-6 text-center text-sm leading-relaxed text-gray-700 dark:text-gray-300">
		{description}
	</p>

	<!-- Event Details Section -->
	<!-- Event Details Section -->
	<div
		class="grid grid-cols-2 gap-6 rounded-2xl bg-gradient-to-r from-gray-100 to-gray-300 p-6 text-gray-900 shadow-lg dark:from-gray-800 dark:to-gray-900 dark:text-white"
	>
		<div class="flex items-center gap-3">
			<span class="text-lg">📍</span>
			<span class="font-semibold">{hostedBy}</span>
		</div>

		<div class="flex items-center gap-3">
			<span class="text-lg">📅</span>
			<span class="font-semibold">{eventDate}</span>
		</div>

		<div class="flex items-center gap-3">
			<span class="text-lg">🏷️</span>
			<span class="text-gray-700 dark:text-gray-300">{eventTags}</span>
		</div>

		<div class="flex items-center gap-3">
			<span class="text-lg">⏳</span>
			<span class="text-gray-700 dark:text-gray-300">{eventTime}</span>
		</div>

		<div class="flex items-center gap-3">
			<span class="text-lg">📌</span>
			<span class="text-gray-700 dark:text-gray-300">{eventLocation}</span>
		</div>

		<div class="flex items-center gap-3">
			<span class="text-lg">👥</span>
			<span class="text-gray-700 dark:text-gray-300">{attendees}</span>
		</div>
	</div>

	<!-- Action Buttons -->
	<div class="mt-6 flex justify-between gap-4">
		<button
			class="w-1/2 rounded-xl bg-gray-300 py-3 font-medium text-gray-900 transition-all hover:bg-gray-400 dark:bg-gray-700 dark:text-white dark:hover:bg-gray-600"
		>
			View Event
		</button>
		<button
			class="w-1/2 rounded-xl bg-blue-600 py-3 font-medium text-white transition-all hover:bg-blue-700"
		>
			Sign Me Up
		</button>
	</div>
</div>
