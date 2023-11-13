// stats1.js
const renderChart1 = (data, labels) => {
    var ctx1 = document.getElementById("myChart1").getContext("2d");
    
    // Destroy previous Chart instance if it exists
    ctx1.clearRect(0, 0, ctx1.canvas.width, ctx1.canvas.height);
  
    window.myChart1 = new Chart(ctx1, {
      type: "doughnut",
      data: {
        labels: labels,
        datasets: [
          {
            label: "Last 6 months expenses",
            data: data,
            backgroundColor: [
              "rgba(255, 99, 132, 0.2)",
              "rgba(54, 162, 235, 0.2)",
              "rgba(255, 206, 86, 0.2)",
              "rgba(75, 192, 192, 0.2)",
              "rgba(153, 102, 255, 0.2)",
              "rgba(255, 159, 64, 0.2)",
            ],
            borderColor: [
              "rgba(255, 99, 132, 1)",
              "rgba(54, 162, 235, 1)",
              "rgba(255, 206, 86, 1)",
              "rgba(75, 192, 192, 1)",
              "rgba(153, 102, 255, 1)",
              "rgba(255, 159, 64, 1)",
            ],
            borderWidth: 1,
          },
        ],
      },
      options: {
        title: {
          display: true,
          text: "Expenses per category",
        },
      },
    });
  };
  
  const getChartData1 = () => {
    console.log("fetching");
    fetch("/expense/expense_category_summary")
      .then((res) => res.json())
      .then((results) => {
        console.log("results", results);
        const category_data = results.expense_category_data;
        const [labels, data] = [
          Object.keys(category_data),
          Object.values(category_data),
        ];
  
        renderChart1(data, labels);
      });
  };
  
  document.onload = getChartData1();
  