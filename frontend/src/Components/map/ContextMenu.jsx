import { useEffect } from 'react'

export default  function ContextMenu({ x, y, onClearAll, onClose }) {

    // Close on any click or Escape
    useEffect(() => {

        function handle(e){
            if (e.type === 'keydown' && e.key !== 'Escape') return
            onClose()
        }

        document.addEventListener('click', handle)
        document.addEventListener('keydown', handle)

        return () => {
            document.removeEventListener('click', handle)
            document.removeEventListener('keydown', handle)
        }

    }, [])


    return (
        <div className='context-menu' style={{ top: y, left: x}}>
            <button
                className='item'
                onClick={() => {
                    onClose()
                }}
            >
                🗑️ Clear All Selections
            </button>
        </div>
    )
}

