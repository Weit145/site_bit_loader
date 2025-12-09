import './button_handler.css'
import type { ReactNode, MouseEvent, CSSProperties } from 'react'

type ButtonProps = {
    className?: string
    children: ReactNode
    onClick?: (e: MouseEvent<HTMLButtonElement>) => void
    type?: 'button' | 'submit' | 'reset'
    flag_disabled?: boolean
    style?: CSSProperties
}

export default function Button({ className, children, onClick, type = 'button', flag_disabled = false, style }: ButtonProps) {
    return (
        <button
            className={className ?? 'Button'}
            onClick={onClick}
            type={type}
            disabled={flag_disabled}
            style={style}
        >
            {children}
        </button>
    )
}
