<script lang="ts">
	export let value = ''; // Input value
	export let type = 'text'; // Input type eg. text, email, password
	export let placeholder = ''; // Placeholder Value
	export let Name = ''; // Label Text
	export let showLabel = false; // Show Label
	export let required = false; // Is Required Field
	export let minValue: number | undefined = undefined; // Min Value for Number Input
	export let maxValue: number | undefined = undefined; // Max Value for Number Input
	export let invalid = false; // Is Data Invalid

	let inputElement: HTMLInputElement;

	// Check if Input is Valid
	export function reportValidity() {
		let valid = inputElement.reportValidity();
		if (!valid) {
			console.log('Invalid');
			invalid = true;
			inputElement.focus();
		} else {
			invalid = false;
		}
		console.log('Type: ', type, ' Value: ', value, ' Valid: ', valid);
		return valid;
	}

	// Set Error Message
	export function setErrorMessage(message: string) {
		console.log('Setting error message: ', message);
		inputElement.setCustomValidity(message);
	}
</script>

<div class="mt-4">
	{#if showLabel}
		<label for={Name} class="block text-gray-700">{Name} </label>
	{/if}

	<input
		{type}
		id={Name}
		name={Name}
		{placeholder}
		bind:value
		{required}
		class="mt-2 w-full rounded-md border px-4 py-2 focus:ring-1 focus:ring-blue-600 focus:outline-none {!invalid
			? 'border-black'
			: 'border-red-600'}"
		{...type === 'number' ? { min: minValue, max: maxValue } : {}}
		bind:this={inputElement}
	/>
</div>
