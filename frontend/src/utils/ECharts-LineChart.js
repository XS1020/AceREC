import * as echarts from 'echarts'
const renderLineChart = function (chartDom ,data) {
    const chartInstance = echarts.init(chartDom)
    chartInstance.resize()
    const xAxisData = data.map(d => d.time)
    const yAxisData = data.map(d => d.value)
    if (xAxisData.length < 3) {
        yAxisData.push(0)
        xAxisData.push(xAxisData[xAxisData.length - 1] + 1)
        yAxisData.splice(0, 0, 0)
        xAxisData.splice(0, 0, xAxisData[0] - 1)
    }
    const option = {
        tooltip: {
            trigger: 'axis',
            position: function (pt) {
                return [pt[0], '10%'];
            }
        },
        grid:{
            top:"20px",
            left:"40px",
            right:"20px",
            bottom:"30px"
        },
        // toolbox: {
        //     feature: {
        //         dataZoom: {
        //             yAxisIndex: 'none'
        //         },
        //         restore: {},
        //         saveAsImage: {}
        //     }
        // },
        xAxis: {
            type: 'category',
            boundaryGap: false,
            data: xAxisData
        },
        yAxis: {
            type: 'value',
        },
        // dataZoom: [{
        //     type: 'inside',
        //     start: 0,
        //     end: 10
        // }, {
        //     start: 0,
        //     end: 10
        // }],
        series: [
            {
                name: 'Citation',
                type: 'line',
                symbol: 'none',
                sampling: 'lttb',
                itemStyle: {
                    color: 'rgb(255, 70, 131)'
                },
                areaStyle: {
                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                        offset: 0,
                        color: 'rgb(255, 158, 68)'
                    }, {
                        offset: 1,
                        color: 'rgb(255, 70, 131)'
                    }])
                },
                data: yAxisData
            }
        ]
    };

    option && chartInstance.setOption(option);
}
export default renderLineChart