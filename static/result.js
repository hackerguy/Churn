$(document).ready(function() {
console.log("ready!");

$('#prediction').html("Prediction = " + "Churn")
$('#probability').html("Probability of Churn = " + "69.90" + "%");
chart(47.14)

	// on form submission ...
  	// $('form').on('submit', function() {
  	$('.onchange').on('change', function() {
     	$('form').submit();
  		console.log("the form has beeen submitted");

  	// grab values
  	Gender = $('input[name="Gender"]').val();
	Status = $('input[name="Status"]').val();
	CarOwner = $('input[name="CarOwner"]').val();
	Paymethod = $('input[name="Paymethod"]').val();
	LocalBilltype = $('input[name="LocalBilltype"]').val();
	LongDistanceBilltype = $('input[name="LongDistanceBilltype"]').val();
	Children = $('input[name="Children"]').val();
	EstIncome = $('input[name="EstIncome"]').val();
	Age = $('input[name="Age"]').val();
	LongDistance  = $('input[name="LongDistance"]').val();
	International = $('input[name="International"]').val();
	Local = $('input[name="Local"]').val();
	Dropped = $('input[name="Dropped"]').val();
	Usage = LongDistance + International + Local
	RatePlan = $('#RatePlan').val();


	console.log(Gender, Status, CarOwner, Paymethod, LocalBilltype, 
			LongDistanceBilltype, Children, EstIncome, Age, LongDistance, International, Local, 
			Dropped, Usage, RatePlan)


  	$.ajax({
  		type: "POST",
  		url: "/",
  		data : { 'Gender': Gender, 'Status': Status, 'CarOwner': CarOwner, 'Paymethod': Paymethod, 
  			'LocalBilltype': LocalBilltype, 'LongDistanceBilltype': LongDistanceBilltype, 
  			'Children': Children, 'EstIncome': EstIncome, 'Age': Age, 'LongDistance': LongDistance, 
  			'International': International, 'Local': Local, 'Dropped': Dropped, 'Usage': Usage, 
  			'RatePlan': RatePlan
			 },

		success: function(results) {
			if (results.probability) {
				console.log("probability success");
				
				if (results.prediction ===1) {
    				prediction = "Not Churn";
    			} else {
    				prediction = "Churn";
    			}

    			$('#prediction').html("Prediction = " + prediction)
				$('#probability').html("Probability of Churning = " + (results.probability*100).toFixed(2) + "%");
				chart(results.probability)

			} else {
				console.log("Something went wrong with the prediction");
				$('.result').html('Something went wrong with the prediction.')
			}
		},

		error: function(error) {
			console.log(error)
		}

		});
	
	});

});