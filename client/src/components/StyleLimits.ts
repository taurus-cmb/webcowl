/**
 * Class that will return component styles based on ranges
 */
export class StyleLimits {
  limits: RangeLimits;
  styles: RangeStyles;

  constructor(limits: RangeLimits, styles: RangeStyles) {
    this.limits = limits;
    this.styles = styles;
  }

  getStyle(value: number) {
    if (value < this.limits.xlo) {
      return this.styles.xlo;
    } else if (value > this.limits.xhi) {
      return this.styles.xhi;
    } else if (value < this.limits.lo) {
      return this.styles.lo;
    } else if (value > this.limits.hi) {
      return this.styles.hi;
    } else {
      return {};
    }
  }
}

export interface RangeLimits {
  xlo: number;
  lo: number;
  hi: number;
  xhi: number;
}

export interface RangeStyles {
  xlo: {};
  lo: {};
  hi: {};
  xhi: {};
}
