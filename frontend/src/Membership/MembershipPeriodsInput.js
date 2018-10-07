import React from 'react';
import {assert} from "../utils";
import * as _ from "underscore";
import DatePeriod from "../Models/DatePeriod";
import DatePeriodList from "../Models/DatePeriodList";
import DatePeriodListInput from "../Components/DatePeriodListInput";


// Return true if span1 end overlaps or is adjacent to span2 start.
export const isConnected = (span1, span2) => {
    assert(span1.start <= span2.start);
    return span2.start - span1.end <= 24 * 3600 * 1000;
};


// Return assembled periods for non deleted spans in a category.
export const filterPeriods = (items, category) => {
    const spans = items.filter(i => !i.deleted_at &&  i.span_type === category).sort((a, b) => a.startdate > b.startdate);
    const periods = [];
    
    while (!_.isEmpty(spans)) {
        let i = 1;
        while (i < spans.length && isConnected(spans[i - 1], spans[i])) ++i;
        const periodSpans = spans.splice(0, i);
        periods.push(new DatePeriod({
                                    start: new Date(Math.min(...periodSpans.map(s => s.start))),
                                    end: new Date(Math.max(...periodSpans.map(s => s.end))),
                                }));
    }
    return periods;
};


export default class MembershipPeriodsInput extends React.Component {
    constructor(props) {
        super(props);
        this.unsubscribe = [];
        this.categories = [
            new DatePeriodList({category: 'labaccess'}),
            new DatePeriodList({category: 'membership'}),
            new DatePeriodList({category: 'special_labaccess'}),
        ];
        this.state = {showHistoric: true, saveDisabled: true};
    }

    componentDidMount() {
        this.unsubscribe.push(this.props.spans.subscribe(({items}) => {
            this.categories.forEach(periods => periods.replace(filterPeriods(items, periods.category)));
        }));
        this.categories.forEach(category => {
            this.unsubscribe.push(category.subscribe(() => this.setState({saveDisabled: !this.categories.some(c => c.isDirty())})));
        });
    }

    componentWillUnmount() {
        this.unsubscribe.forEach(u => u());
    }

    render() {
        const {showHistoric, saveDisabled} = this.state;
        return (
            <form className="uk-form">
                <label className="uk-label" htmlFor="showHistoric">Visa historiska</label>
                <input id="showHistoric" className="uk-checkbox" type="checkbox" checked={showHistoric} onChange={e => this.setState({showHistoric: e.target.checked})}/>
                {this.categories.map(periods => <DatePeriodListInput key={periods.category} periods={periods} showHistoric={showHistoric}/>)}
                <button disabled={saveDisabled} className="uk-button uk-button-success uk-float-right"><i className="uk-icon-save"/> Spara</button>
            </form>
        );
    }
}

