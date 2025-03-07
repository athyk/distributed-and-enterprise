<script lang="ts">
	import Input from '$components/FormInput/Input.svelte';
	import Button from '$components/SubmitButton/button.svelte';
	import { post } from '$lib/Api/post';
	import Page1 from './Pages/page1.svelte';
	import Page2 from './Pages/page2.svelte';
	import Page3 from './Pages/page3.svelte';
	import Page4 from './Pages/page4.svelte';
	import type { response } from '$lib/Api/types';
	import Popup from '$components/ErrorPopUp/popup.svelte';

	let email = '';
	let password = '';
	let passwordConfirm = '';

	let fName = '';
	let lName = '';
	let dob = '';
	let gender: string[] = [];

	let degree: string[] = [];
	let degreeYear = '';
	let graduationYear = '';

	let tags: string[] = [];

	let otp: string[] = [];

	let step = 1;
	let maxstep = 4;

	let page1Inputs: Input[] = [];
	let page2Inputs: Input[] = [];
	let page3Inputs: Input[] = [];

	let pageInputs = [page1Inputs, page2Inputs, page3Inputs];

	let errorMessage = '';

	function checkPageValidity() {
		let valid = true;
		console.log(pageInputs[step - 1]);
		pageInputs[step - 1].forEach((input) => {
			console.log(input);
			if (!input.reportValidity()) {
				console.log('Invalid');
				valid = false;
			}
		});
		console.log('Page Valid: ', valid);
		if (step === 1 && valid) {
			valid = password === passwordConfirm;
			console.log('Password Match: ', valid);
			page1Inputs[1].setErrorMessage("Password doesn't match");
			page1Inputs[2].setErrorMessage("Password doesn't match");
		}
		console.log('Password Valid: ', valid);
		if (valid) {
			step = Math.min(maxstep, step + 1);
		}
		console.log(valid);
		return valid;
	}

	async function handleSubmit() {
		dob = dob.split('-').reverse().join('-');
		graduationYear = '30-06-' + graduationYear;

		let data = {
			email: email,
			password: password,
			first_name: fName,
			last_name: lName,
			dob: dob,
			gender: gender[0],
			degree: degree[0],
			year_of_study: degreeYear,
			grad_year: graduationYear,
			tag: tags
		};
		console.log(data);

		try {
			let response = (await post('authorisation/register', data)) as response;
			console.log(response);
			if (response.http_status === 201) {
				alert('Registration Successful');
				step = 1;
			} else if (response.http_status === 400) {
				if (response.error_message.includes('Email Already Exists')) {
					errorMessage = 'Email Already Exists';
				} else {
					errorMessage = response.error_message.join(', ');
				}
			} else {
				errorMessage = 'An error occurred';
			}
		} catch (error) {
			console.error(error);
			errorMessage = 'An unexpected error occurred';
		}
	}
</script>

{step}
<div class="w-full p-8 md:mx-auto md:w-1/2">
	<h2 class="text-center text-2xl font-semibold text-gray-700">Register</h2>
	<Popup bind:errorMessage />
	<p class="text-center text-xl text-gray-600">Fill in User Info</p>
	<form on:submit|preventDefault={handleSubmit}>
		{#if step === 1}
			<Page1 bind:email bind:password bind:passwordConfirm bind:pageInputs={page1Inputs} />
		{/if}

		{#if step === 2}
			<Page2 bind:fName bind:lName bind:dob bind:gender bind:pageInputs={page2Inputs} />
		{/if}

		{#if step === 3}
			<Page3
				bind:degree
				bind:degreeYear
				bind:graduationYear
				bind:tags
				bind:pageInputs={page3Inputs}
			/>
		{/if}
		{#if step === 4}
			<Page4 bind:otp />
		{/if}

		<div class="mt-4 flex flex-col items-center justify-between space-y-2 md:flex-row md:space-y-0">
			{#if step === 1}
				<a href="/login" class="text-sm text-gray-600 hover:text-gray-900"
					>Already have an Account?</a
				>
			{/if}
			{#if step > 1}
				<Button type="button" text="Previous Step" onClick={() => (step = Math.max(1, step - 1))} />
			{/if}

			{#if step === maxstep}
				<Button />
			{:else}
				<Button type="button" text="Next Step" onClick={checkPageValidity} />
			{/if}
		</div>
	</form>
</div>
