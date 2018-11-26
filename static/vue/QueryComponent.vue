<template>
    <div class="query">
        <h2>Query {{ query }}</h2>
        <div class='inputs' v-if='need_input'>
            <div class="row" v-for="i in inputs">
                {{ i }}:
                <input type="text" :id='query+ "_" + i'>
            </div>
        </div>
        <br>
        <button class="btn" @click="make_query">Make query</button>
        <table v-if="response_result" border="1">
            <tr>
                <th v-for="i in labels">{{ i }}</th>
            </tr>
            <tr v-for="row in data_">
                <td v-for="el in row"> {{ el }}</td>
            </tr>
        </table>
    </div>
</template>

<script>
export default {
    name: "QueryComponent",
    props: ['query'],
    data:function() {
        var inputs = [
            ['username'],
            ['date'],
            ['start','end'],
            ['username'],
            ['date'],
            [],
            [],
            ['date'],
            ['period'],
            [],
        ]

        console.log(inputs);
        return {
            labels: [
                'test',
                'test2'
            ],
            data_ : [
                ['test', 'tsnahuoet'],
                ['astonhusnao', 'shaotheusnth'],
            ],
            need_input: inputs[this.query -1 ].length != 0,
            inputs: inputs[this.query -1 ],
            response_result: false,
        }
    },
    methods: {
        make_query: function(el) {
            var query_set = "";
            this.inputs.forEach(input => {
                var val = document.getElementById(this.query + "_" + input).value;
                query_set += input + "=" + val + "&";
            });
            var parent = this;
            this.$http.get('/query' + this.query + '?' + query_set).then(response => {
                if(this.query != 6){
                    var data = response.body;
                    parent.labels = data[0];
                    parent.data_ = data[1];
                    parent.response_result = true;
                }else {
                    var data = response.body;
                    parent.labels = [];
                    parent.data_ = data;
                    console.log(parent.data_);
                    parent.response_result = true;
                }
            }, response => {
                console.log(response.body);
            });
        }
    }
}

</script>
