let ZoominfoSearchContactResult = (() => {
	const _baseUrl = '/contact/';

	const sendRequest = (endPoint, params, callback) => {
		$.ajax({
			url : _baseUrl + endPoint,
			data : params,
			dataType: 'json',
			type : "POST",
			success : (response) => {
				if (!response.status) {
					
				}
				else if (typeof callback === 'function') {
					callback(response);
				}
			},
			error : (error) => {
				// alert("Something went wrong....");
			},
		});
	}

	// const navProved = (val) => {
	// 	sendRequest("navProvedAjax/", {"val" : val}, (response) => {
	// 		drawDataTable(response)
	// 	});
	// }

	const init = () => {
		$(document)
		.on("click", "#contact-result", (event) => {
            
		})
	}

	return {
		init : init
	}
})();

((window, $) => {		
	ZoominfoSearchContactResult.init();
})(window, jQuery);