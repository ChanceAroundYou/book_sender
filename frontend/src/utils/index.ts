const renderSeries = (value: string, with_mark: boolean = false) => {
    if (value.includes('_')) {
        const series = value.split('_').map((word: string) => word.charAt(0).toUpperCase() + word.slice(1)).join(' ').replace('Usa', 'USA').replace('Uk', 'UK');
        if (with_mark) {
            return series + ' 系列';
        }
        return series;
    }
    return value;
};

export { renderSeries };